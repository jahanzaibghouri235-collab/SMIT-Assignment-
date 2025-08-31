from datetime import datetime as dt

def logger(func):
    def wrapper(*args, **kwargs):
        with open("log.txt","a") as log_file:
            running_log = f"{dt.now()} Executed'{func.__name__}'\n"
            result = func(*args,**kwargs)
            log_file.write(running_log)
        return result
    return wrapper

class Order:
    def __init__(self):
        self.order = []

    @logger
    def add_item_by_id(self, product_id, quantity):
        with open('products.csv', 'r') as file:
            lines = file.readlines()[1:]
            for line in lines:
                product = line.strip().split(',')
                if product[0] and int(product[0]) == product_id:
                    total_price = float(product[2]) * quantity
                    self.order.append({
                        "product_id": product_id,
                        "name": product[1],
                        "quantity": quantity,
                        "total": total_price
                    })
                    with open("log.txt","a") as file:
                        addeditem = f"{dt.now()} Added Item : '{product[1]}'(x {quantity})' Total '{total_price}'\n"
                        file.write(addeditem)
                    break

    discountrate = 0
    @classmethod
    @logger
    def set_discount(cls,discountrate):
        cls.discountrate = discountrate
        with open("log.txt","a") as file:
            file.write(f"{dt.now()} Discount set to {discountrate * 100}%\n")

    @logger
    def calculate_total(self):
        total = sum(product["total"] for product in self.order)
        discount_rate = total * self.discountrate
        finaltotal = total - discount_rate
        with open("log.txt","a") as file:
            file.write(f"{dt.now()} Total after discount {finaltotal}\n")
        return finaltotal

    @staticmethod
    def is_invalid_id(product_id):
        with open('products.csv', 'r') as file:
            lines = file.readlines()[1:]
            for line in lines:
                product = line.strip().split(',')
                if product[0] and int(product[0]) == product_id:
                    return False
        with open("log.txt","a") as file:
            file.write(f"{dt.now()} Invalid product ID Attempt {product_id}\n")
        return True

order = Order()
order.add_item_by_id(2, 2)
print(order.order)
order.set_discount(0.1)
print(order.calculate_total())
print(order.is_invalid_id(55))
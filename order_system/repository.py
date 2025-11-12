class Repository:
    """
    Простое in-memory хранилище.
    Реализует добавление продуктов, создание заказов, пометку оплаты и получение заказа.
    """
    def __init__(self):
        self.products = {}
        self.orders = {}
        self.next_order_id = 1

    def add_product(self, product):
        if product.id in self.products:
            raise ValueError("Product with same id already exists")
        self.products[product.id] = product

    def create_order(self, product_id, quantity):
        if product_id not in self.products:
            raise ValueError("Product not found")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        order_id = self.next_order_id
        self.next_order_id += 1
        order = {"id": order_id, "product_id": product_id, "quantity": quantity, "paid": False}
        self.orders[order_id] = order
        return order

    def mark_paid(self, order_id):
        if order_id not in self.orders:
            raise ValueError("Order not found")
        self.orders[order_id]["paid"] = True
        return self.orders[order_id]

    def get_order(self, order_id):
        return self.orders.get(order_id)

class OrderService:
    """
    Создание заказа и оплата.
    Отвечает за координацию репозитория и уведомлений.
    """
    def __init__(self, repo, notifier):
        self.repo = repo
        self.notifier = notifier

    def create_order(self, product_id, quantity):
        order = self.repo.create_order(product_id, quantity)
        try:
            self.notifier.send(f"Order #{order['id']} created.")
        except Exception:
            pass
        return order

    def pay_order(self, order_id):
        order = self.repo.mark_paid(order_id)
        try:
            self.notifier.send(f"Order #{order_id} has been paid.")
        except Exception:
            pass
        return order

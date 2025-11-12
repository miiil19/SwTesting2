class NotificationService:
    """
    Имитация внешнего сервиса уведомлений.
    Хранит отправленные сообщения в списке sent_notifications для проверок в тестах.
    """
    def __init__(self):
        self.sent_notifications = []

    def send(self, message):
        self.sent_notifications.append(message)
        return True

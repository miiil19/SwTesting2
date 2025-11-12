import pytest
from order_system.models import Product
from order_system.repository import Repository
from order_system.services import OrderService
from order_system.notifications import NotificationService

@pytest.fixture
def setup_system():
    repo = Repository()
    notifier = NotificationService()
    service = OrderService(repo, notifier)
    # добавим тестовый товар
    repo.add_product(Product(id=1, name="Laptop", price=1000.0))
    return repo, notifier, service

def test_order_creation_integration(setup_system):
    """
    Успешный сценарий: создание заказа -> запись в репозиторий -> уведомление
    """
    repo, notifier, service = setup_system
    order = service.create_order(1, 2)
    # Проверяем, что заказ записан в хранилище
    saved_order = repo.get_order(order['id'])
    assert saved_order is not None
    assert saved_order['quantity'] == 2
    assert saved_order['product_id'] == 1
    assert saved_order['paid'] is False
    # Проверяем, что уведомление отправлено и содержит ключевое слово
    assert len(notifier.sent_notifications) == 1
    assert "created" in notifier.sent_notifications[-1]

def test_order_payment_integration(setup_system):
    """
    Успешный сценарий: оплата заказа -> обновление состояния -> уведомление
    """
    repo, notifier, service = setup_system
    order = service.create_order(1, 1)
    # оплатим заказ
    updated = service.pay_order(order['id'])
    assert updated['paid'] is True
    # проверяем, что последнее уведомление о платеже
    assert "paid" in notifier.sent_notifications[-1]

def test_invalid_product_error_propagation(setup_system):
    """
    Oшибочный сценарий: попытка создать заказ для несуществующего продукта.
    Ожидается ValueError, который возникает в repository.
    """
    _, _, service = setup_system
    with pytest.raises(ValueError) as excinfo:
        service.create_order(99, 1)
    assert "Product not found" in str(excinfo.value)

def test_notification_sequence(setup_system):
    """
    Проверка последовательности уведомлений: создание -> оплата.
    """
    repo, notifier, service = setup_system
    order = service.create_order(1, 1)
    service.pay_order(order['id'])
    assert notifier.sent_notifications == [
        f"Order #{order['id']} created.",
        f"Order #{order['id']} has been paid."
    ]

def test_repository_state_isolated_between_orders(setup_system):
    """
    Проверяет, что репозиторий корректно хранит несколько заказов,
    id разных заказов не совпадают.
    """
    repo, notifier, service = setup_system
    o1 = service.create_order(1, 1)
    o2 = service.create_order(1, 3)
    assert o1['id'] != o2['id']
    assert len(repo.orders) == 2
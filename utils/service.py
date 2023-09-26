from robots.models import Robot
from utils.models_utils import filter_model, get_or_create_model
from orders.models import Customer, Order
from orders.tasks import send_notification_email


class OrderService:
    def __init__(self, email, robot_serial):
        self.email = email
        self.robot_serial = robot_serial

    def get_or_create_customer(self):
        return get_or_create_model(Customer, email=self.email)

    def get_or_create_order(self, customer):
        return get_or_create_model(
            Order, customer=customer, robot_serial=self.robot_serial
        )

    def process_order(self):
        customer, _ = self.get_or_create_customer()
        _, created_order = self.get_or_create_order(customer)

        robot = filter_model(Robot, serial=self.robot_serial)

        if robot and created_order:
            return "Заказ сформирован."
        elif robot:
            return "Заказ уже существует."
        else:
            send_notification_email.delay(self.email, self.robot_serial)
            return "Такого робота пока нет в наличии. Как только он появится, мы пришлем вам сообщение на email."

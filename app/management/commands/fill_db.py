import random

from django.core import management
from django.core.management.base import BaseCommand
from ...models import *
from .utils import random_date, random_timedelta


def add_students():
    Student.objects.create(
        name="Винокуров Дмитрий",
        faculty="ИУ",
        group="ИУ5-32",
        image="students/1.png"
    )

    Student.objects.create(
        name="Москвина Арина",
        faculty="МТ",
        group="МТ7-61",
        image="students/2.png"
    )

    Student.objects.create(
        name="Авентьев Максим",
        faculty="СМ",
        group="CМ3-15",
        image="students/3.png"
    )

    Student.objects.create(
        name="Фролова Вера",
        faculty="ИУ",
        group="ИУ6-24",
        image="students/4.png"
    )

    Student.objects.create(
        name="Медведев Александр",
        faculty="ИБМ",
        group="ИБМ8-73",
        image="students/5.png"
    )

    print("Услуги добавлены")


def add_orders():
    owners = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(owners) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    students = Student.objects.all()

    for _ in range(30):
        order = Order.objects.create()
        order.status = random.randint(2, 5)
        order.owner = random.choice(owners)

        if order.status in [3, 4]:
            order.date_complete = random_date()
            order.date_formation = order.date_complete - random_timedelta()
            order.date_created = order.date_formation - random_timedelta()
            order.moderator = random.choice(moderators)
        else:
            order.date_formation = random_date()
            order.date_created = order.date_formation - random_timedelta()

        for i in range(random.randint(1, 3)):
            order.students.add(random.choice(students))

        if order.status in [2, 3, 4]:
            order.visa = random.randint(0, 2)

        order.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_students()
        add_orders()










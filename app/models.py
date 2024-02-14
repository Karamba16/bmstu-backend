from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.db import models

from django.utils import timezone


class Student(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="ФИО")
    faculty = models.CharField(max_length=6, verbose_name="Факультет")
    group = models.CharField(max_length=10, verbose_name="Группа")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(upload_to="students", default="students/default.png", verbose_name="Фото")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('name', name)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_moderator = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Order(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )

    VISA_CHOICES = (
        (0, 'Не получилось определить'),
        (1, 'В наличии'),
        (2, 'Отсутствует')
    )

    visa = models.IntegerField(choices=VISA_CHOICES, verbose_name="Виза", null=True, blank=True)

    students = models.ManyToManyField(Student, verbose_name="Студенты", null=True)

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner', null=True)
    moderator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Модератор", related_name='moderator', blank=True,  null=True)

    def __str__(self):
        return "Приказ №" + str(self.pk)

    class Meta:
        verbose_name = "Приказ"
        verbose_name_plural = "Приказы"
        ordering = ('-date_formation', )
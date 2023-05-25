from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to='login/static/images/', blank=True)


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    time = models.DateTimeField(default=timezone.now)
    CATEGORIES = [
        ("Зарплата", "Зарплата"),
        ("Бізнес", "Бізнес"),
        ("% з депозиту", "% з депозиту"),
        ("Подарунки", "Подарунки"),
        ("Інвестиції", "Інвестиції"),
        ("Інше", "Інше"),
    ]
    category = models.CharField(max_length=100, choices=CATEGORIES)
    PAYMENT_METHOD = [
        ("CASH", "Готівка"),
        ("CARD", "Картка"),
        ("DEPO", "Депозит"),
    ]
    paymentMethod = models.CharField(max_length=4, choices=PAYMENT_METHOD)


class Spending(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    time = models.DateTimeField(default=timezone.now)
    CATEGORIES = [
        ("Харчування", "Харчування"),
        ("Житло", "Житло"),
        ("Зв'язок", "Зв'язок"),
        ("Транспорт", "Транспорт"),
        ("Відпочинок", "Відпочинок"),
        ("Цілі", "Цілі"),
    ]
    category = models.CharField(max_length=100, choices=CATEGORIES)
    PAYMENT_METHOD = [
        ("CASH", "Готівка"),
        ("CARD", "Картка"),
        ("DEPO", "Депозит"),
    ]
    paymentMethod = models.CharField(max_length=4, choices=PAYMENT_METHOD)

class Saving(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    time = models.DateTimeField(default=timezone.now)
    CATEGORIES = [
        ("Готівка", "Готівка"),
        ("Картка", "Картка"),
        ("Депозит", "Депозит"),
    ]
    category = models.CharField(max_length=100, choices=CATEGORIES)
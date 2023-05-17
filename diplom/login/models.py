from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    time = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=100)
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
    category = models.CharField(max_length=100)
    PAYMENT_METHOD = [
        ("CASH", "Готівка"),
        ("CARD", "Картка"),
        ("DEPO", "Депозит"),
    ]
    paymentMethod = models.CharField(max_length=4, choices=PAYMENT_METHOD)

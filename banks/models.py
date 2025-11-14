from django.db import models
from django.contrib.auth.models import User


class Bank(models.Model):
    name = models.CharField(max_length=200)
    swift_code = models.CharField(max_length=200)
    institution_number = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='banks')

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=200)
    transit_number = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email = models.EmailField(default='admin@utoronto.ca')
    capacity = models.PositiveIntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='branches')

    def __str__(self):
        return self.name


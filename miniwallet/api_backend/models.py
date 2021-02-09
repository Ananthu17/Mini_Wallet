from django.db import models
from rest_framework.authtoken.models import Token

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length = 50,blank=True,null=True)
    customer_xid = models.CharField(max_length = 50)
    token = models.OneToOneField(Token, on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.customer_xid

class Wallet(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE,blank=True,null=True)
    balance = models.IntegerField(default=0)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.customer

class Transaction(models.Model):
    amount = models.IntegerField()
    reference_id = models.CharField(max_length = 50)

    def __str__(self):
        return self.amount

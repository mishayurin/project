from django.db import models


# In this model file to communicate with the database

class Client(models.Model):
    # id = models.AutoField()
    Client_ID = models.AutoField()
    Phone = models.SlugField(max_length=25)
    Email = models.EmailField(max_length=254)
    Date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    Full_name = models.CharField(max_length=255)
    Wallet_balance = models.BigIntegerField()


class Expenses(models.Model):
    Expenses_ID = models.AutoField()
    Amount = models.IntegerField()  # models.PositiveIntegerField()
    Expense_Date = models.DateTimeField(auto_now_add=True)
    Client_ID = models.AutoField()
    Limits_ID = models.AutoField()
    Expenses_types_ID = models.models.AutoField()


class Expenses_Types(models.Model):
    Expenses_types_ID = models.AutoField()
    Category = models.CharField(max_length=255)
    Name_of_expenses_types = models.CharField(max_length=255)


class Limits(models.Model):
    Limits_ID = models.AutoField()
    Amount_of_limit = models.IntegerField()
    Date_time_gap = models.DateTimeField()

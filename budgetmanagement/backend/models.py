from django.db import models


# In this model file to communicate with the database

class Client(models.Model):
    Client_ID = models.AutoField(primary_key=True)
    Phone = models.SlugField(max_length=25)
    Email = models.EmailField(max_length=254)
    Date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    Full_name = models.CharField(max_length=255)
    Wallet_balance = models.BigIntegerField()


class Expenses_Types(models.Model):
    Expenses_types_ID = models.AutoField(primary_key=True)
    Category = models.CharField(max_length=255)
    Name_of_expenses_types = models.CharField(max_length=255)


class Limits(models.Model):
    Limits_ID = models.AutoField(primary_key=True)
    Amount_of_limit = models.IntegerField()
    Date_time_gap = models.DateTimeField()


class Expenses(models.Model):
    Expenses_ID = models.AutoField(primary_key=True)
    Amount = models.IntegerField()  # models.PositiveIntegerField()
    Expense_Date = models.DateTimeField(auto_now_add=True)
    Client_ID = models.ForeignKey(Client, on_delete = models.CASCADE)
    Limits_ID = models.ForeignKey(Limits, on_delete = models.CASCADE)
    Expenses_types_ID = models.ForeignKey(Expenses_Types, on_delete = models.CASCADE)

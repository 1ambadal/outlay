from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255,default="")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    current_date = models.DateField(default = datetime.datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

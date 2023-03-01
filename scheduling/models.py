import django

from django.db import models
from datetime import datetime    

class Pharmacy(models.Model):
    name = models.CharField(max_length=100,unique=True)
    area = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Shift(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE,blank=True,null=True)
    start_time = models.TimeField(default=datetime.now())
    end_time = models.TimeField(default=datetime.now())
    capacity = models.PositiveBigIntegerField(default = 0,editable=False)
    max_capacity = models.PositiveBigIntegerField(default= 0)
    
class Student(models.Model):
    id = models.IntegerField(primary_key=True,unique=True)
    name = models.CharField(max_length=50)
    preferred_area = models.CharField(max_length=50,blank=True)
    preferred_start_time = models.TimeField(default=datetime.now(),blank=True)
    assigned_shift = models.ForeignKey(Shift, on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.name
    
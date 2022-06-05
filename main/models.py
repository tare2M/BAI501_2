from statistics import mode
from django.db import models
from django.urls import reverse



class graph(models.Model):

    city_name1 = models.CharField(max_length=50)
    city_name2 = models.CharField(max_length=50)
    actual_distance = models.IntegerField()
    def __str__(self):
        return self.city_name1

class heuristic(models.Model):

    heuristic_name = models.CharField(max_length=50)
    heuristic_value = models.IntegerField()
    def __str__(self):
        return self.heuristic_name

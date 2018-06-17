# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Player(models.Model):
    salary = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=10)
    points = models.FloatField()
    value = models.FloatField()
    team = models.CharField(max_length=50)

    def __str__(self):
        return self.name

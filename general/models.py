# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Player(models.Model):
    uid = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    salary = models.IntegerField()
    position = models.CharField(max_length=10)
    points = models.FloatField()
    value = models.FloatField()
    team = models.CharField(max_length=50)
    updated_at = models.DateField(auto_now=True)
    game_category = models.IntegerField(default=0)

    class Meta:
        unique_together = ('name', 'team')

    def __str__(self):
        return self.uid or self.name

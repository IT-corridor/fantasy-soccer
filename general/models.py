# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Player(models.Model):
    uid = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    salary = models.IntegerField()
    position = models.CharField(max_length=10)
    points = models.FloatField(default=0)
    value = models.FloatField(default=0)
    team = models.CharField(max_length=50)
    updated_at = models.DateField(auto_now=True)
    game_category = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'team')

    def __str__(self):
        return self.uid or self.name


class PlayerList(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

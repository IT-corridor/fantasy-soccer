# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from general.models import *


def players(request):
	players = Player.objects.all()
	return render(request, 'players.html', locals())

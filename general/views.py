# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from general.models import *


def players(request):
    players = Player.objects.all()
    return render(request, 'players.html', locals())

def gen_lineups(request):
    rosters = []
    ids = request.POST.getlist('ids')
    ids = [int(ii) for ii in ids]
    players = Player.objects.filter(id__in=ids)
    return render(request, 'lineups.html', locals())


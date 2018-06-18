# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

from general.models import *
from general.lineup import *

def players(request):
    players = Player.objects.all()
    return render(request, 'players.html', locals())

def gen_lineups(request):
    rosters = []
    ids = request.POST.getlist('ids')
    num_lineups = int(request.POST.get('num-lineups'))
    ids = [int(ii) for ii in ids]
    players = Player.objects.filter(id__in=ids)
    lineups = calc_lineups(players, num_lineups)
    total_num_lineups = 339
    avg_points = lineups[0].projected()

    return HttpResponse(render_to_string('player-lineup.html', locals()))

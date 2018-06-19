# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import mimetypes

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
from django.contrib.contenttypes.models import ContentType

from general.models import *
from general.lineup import *

def players(request):
    players = Player.objects.all().exclude(uid__isnull=True)
    return render(request, 'players.html', locals())

def gen_lineups(request):
    rosters = []
    ids = request.POST.getlist('ids')
    num_lineups = int(request.POST.get('num-lineups'))
    ids = [int(ii) for ii in ids]
    players = Player.objects.filter(id__in=ids)
    lineups = calc_lineups(players, num_lineups)
    total_num_lineups = get_total_num_lineups(players)
    avg_points = lineups[0].projected() if lineups else 0

    return HttpResponse(render_to_string('player-lineup.html', locals()))

def export_lineups(request):
    ids = request.POST.getlist('ids')
    num_lineups = int(request.POST.get('num-lineups'))
    ids = [int(ii) for ii in ids]
    players = Player.objects.filter(id__in=ids)
    lineups = calc_lineups(players, num_lineups)

    csv_fields = ['FWD', 'FWD', 'MID', 'MID', 'MID', 'DEF', 'DEF', 'GK', 'Projected', 'Salary']
    path = "/tmp/.fantasy_soccer.csv"

    with open(path, 'w') as f:
        f.write(','.join(csv_fields)+'\n')
        for ii in lineups:
            f.write(ii.get_csv())
    
    wrapper = FileWrapper( open( path, "r" ) )
    content_type = mimetypes.guess_type( path )[0]

    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Length'] = os.path.getsize( path ) # not FileField instance
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str( os.path.basename( path ) ) # same here        
    return response

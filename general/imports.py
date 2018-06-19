import csv

from datetime import datetime
from django.http import HttpResponse
from django.conf import settings
from general.models import *


def import_player(request):
    path = settings.BASE_DIR + '/data/roto.csv'

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                obj = Player.objects.create(
                    name = row['player_name'],
                    salary=row['player_salary'],
                    position=row['player_pos'],
                    points=row['player_points'],
                    value=row['player_value'],
                    team=row['player_team'],
                )
            except (Exception) as e:
                print (e)

    return HttpResponse('Successfully imported ({})!'.format(Player.objects.all().count()))

def import_fanduel(path='media/root/Work/Steven/fantasy_soccer/data/FanDuel-FIFA-2018-06-19-26464-players-list'):
    file_name = path.split('/')[-1].strip('.csv')
    fanduel_list = []

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fanduel_list.append([row['Id'], row['Nickname'], row['First Name'], row['Last Name'], row['Team']])

    for ii in Player.objects.all():
        for fi in fanduel_list:
            name_list = ii.name.split(' ')
            if ((ii.name.strip(' GTD') in fi[1]) or (name_list[0] in fi[2] and name_list[-1] in fi[3])) and (ii.team == fi[4]):
                ii.uid = fi[0]
                ii.game_category = ','.join(set((ii.game_category or '').split(',')+[file_name]))
                ii.save()

    print Player.objects.all().exclude(uid__isnull=True).count()
    return file_name

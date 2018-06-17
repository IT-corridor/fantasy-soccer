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

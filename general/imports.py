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
                obj = Demographic.objects.create(
                    mrn=row['MRN'],
                    first_name = row['FirstName'],
                    last_name=row['LastName'],
                    dob=datetime.strptime(row['DOB'], '%m/%d/%Y'),
                    gender=row['Sex'],
                    email=row['Email'],
                    address1=row['Address1'],
                    address2=row['Address2'],
                    city=row['City'],
                    state=row['State'],
                    zip=row['Zip'],
                    phone=row['Phone'],
                    cell_phone=row['cell Phone'],
                    ssn=row['SocialSecurity'],
                )
            except (Exception) as e:
                print (e)

    return HttpResponse('Successfully imported ({})!'.format(Demographic.objects.all().count()))

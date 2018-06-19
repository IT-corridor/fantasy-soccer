"""fantasy_soccer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from general.views import *
from general.imports import *

admin.site.site_header = "Fantasy Soccer"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', players, name="players"),
    url(r'^players', players, name="players"),
    url(r'^import_player', import_player, name="import_player"),
    url(r'^gen-lineups', gen_lineups, name="gen_lineups"),
    url(r'^get-players', get_players, name="get_players"),
    url(r'^upload-csv', upload_csv, name="upload_csv"),
    url(r'^export_lineups', export_lineups, name="export_lineups"),
]

from django.shortcuts import render

from datetime import datetime
import json

from .models import Driver

# Create your views here.

def index(request):
    context = {}
    return render(request, 'index.html', context)

# @require_POST
def matched(request):
    # check if POST objects has longitude and latitude
    if 'latitude' in request.POST and 'longitude' in request.POST:
        latitude = round(request.POST['latitude'],4)
        longitude = round(request.POST['longitude'],4)
        # delete all drivers from previwes run
        Driver.objects.all().delete()
        # area to look for drivers inside it
        left = longitude - 0.02
        right = longitude + 0.02
        top = latitude + 0.02
        bottom  = latitude - 0.02
        # create 10 new random drivers
        for i in range(10):
            Driver.create(left, right, top, bottom)
        drivers = Driver.match_driver(latitude, longitude)

        context = {'message': json.dumps(drivers) }
        return render(request, 'matched.html', context)

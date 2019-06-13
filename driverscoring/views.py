from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from datetime import datetime
import json

from .models import Driver


Number_of_decimal_places_for_coordination = 4
Degree_of_area_around_request = 0.02

# Create your views here.

def index(request):
    context = {}
    return render(request, 'index.html', context)


@csrf_exempt
@require_POST
def matched(request):
    # check if POST objects has longitude and latitude
    if 'latitude' in request.POST and 'longitude' in request.POST:
        latitude = round(float(request.POST['latitude']), Number_of_decimal_places_for_coordination)
        longitude = round(float(request.POST['longitude']), Number_of_decimal_places_for_coordination)
        # delete all drivers from previwes run
        Driver.objects.all().delete()
        # area to look for drivers inside it
        left = longitude - Degree_of_area_around_request
        right = longitude + Degree_of_area_around_request
        top = latitude + Degree_of_area_around_request
        bottom  = latitude - Degree_of_area_around_request
        # create 10 new random drivers
        for i in range(10):
            Driver.create(left, right, top, bottom)
        # sort drivers for based on request
        drivers = Driver.match_driver(latitude, longitude)

        context = {'drivers': drivers }
        return render(request, 'matched.html', context)

from django.db import models

import random
import time
from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt
from decimal import Decimal


Number_of_decimal_places_for_coordination = 4
Degree_of_area_around_request = 0.02
Number_of_decimal_places_for_rating = 2

# Create your models here.

class Driver(models.Model):
    latitude = models.DecimalField(max_digits=Number_of_decimal_places_for_coordination+3, decimal_places=Number_of_decimal_places_for_coordination)
    longitude = models.DecimalField(max_digits=Number_of_decimal_places_for_coordination+3, decimal_places=Number_of_decimal_places_for_coordination)
    rating = models.DecimalField(max_digits=Number_of_decimal_places_for_rating+1, decimal_places=Number_of_decimal_places_for_rating)
    last_trip_time = models.DateTimeField()


    @classmethod
    def create(cls, left, right, top, bottom):
        rating = round(random.uniform(0, 5), Number_of_decimal_places_for_rating)
        longitude = round(random.uniform(left, right), Number_of_decimal_places_for_coordination)
        latitude = round(random.uniform(bottom, top), Number_of_decimal_places_for_coordination)
        # put last trip time some time between yesterday and today
        today = datetime.now()
        yesterday = datetime.now() - timedelta(days=1)
        stime = time.mktime(yesterday.timetuple())
        etime = time.mktime(today.timetuple())
        ptime = stime + random.random() * (etime - stime)
        last_trip_time = datetime.fromtimestamp(ptime)
        driver = cls(latitude=latitude, longitude=longitude, rating=rating, last_trip_time=last_trip_time)
        driver.save()
        return driver

    @classmethod
    def match_driver(cls, latitude, longitude):
        # find all the driveres near request
        score_dict = {}
        drivers = []
        for driver in Driver.objects.all():
            if(abs(float(driver.latitude) - latitude) < Degree_of_area_around_request and abs(float(driver.longitude) - longitude) < Degree_of_area_around_request):
                score = 0
                # convert decimal degrees to radians
                lon1, lat1, lon2, lat2 = map(radians, [float(driver.longitude), float(driver.latitude), longitude, latitude])
                # haversine formula
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * asin(sqrt(a))
                r = 6371
                distance = c * r * 1000
                # calculating score for driver
                # score first is the distance in meters then is divided by rating
                score = distance / float(driver.rating)
                # then for every hour the driver hasn't had a request minus the score by 20
                diff = datetime.now() - driver.last_trip_time
                diff_hours = diff.seconds / 3600
                score -= diff_hours*20
                score_dict[score] = (driver.pk, distance)
        # the lower the score comes first in list
        for i in sorted (score_dict) :
            drivers.append((Driver.objects.filter(pk=score_dict[i][0])[0].as_json(), score_dict[i][1]))
        return drivers


    def as_json(self):
        return dict(
            latitude=float(self.latitude),
            longitude=float(self.longitude),
            rating=float(self.rating),
            last_trip_time=self.last_trip_time.strftime("%Y/%m/%d, %H:%M:%S"))

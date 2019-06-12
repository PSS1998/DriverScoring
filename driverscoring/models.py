from django.db import models

import random
import time
from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt
from decimal import Decimal

# Create your models here.

class Driver(models.Model):
    latitude = models.DecimalField(max_digits=7, decimal_places=4)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    last_trip_time = models.DateTimeField()


    @classmethod
    def create(cls, left, right, top, bottom):
        rating = round(random.uniform(0, 5), 2)
        longitude = round(random.uniform(left, right), 4)
        latitude = round(random.uniform(bottom, top), 4)
        # put last trip time some time between yesterday adn today
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
        id_list = []
        score_list = []
        score_dict = {}
        drivers = []
        for driver in Driver.objects.all():
            if(abs(float(driver.latitude) - latitude) < 0.02 and abs(float(driver.longitude) - longitude) < 0.02):
                score = 0
                id_list.append(driver.id)
                # convert decimal degrees to radians
                lon1, lat1, lon2, lat2 = map(radians, [float(driver.longitude), float(driver.latitude), longitude, latitude])
                # haversine formula
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * asin(sqrt(a))
                r = 6371
                distance = c * r * 1000
                score = distance / float(driver.rating)
                diff = datetime.now() - driver.last_trip_time
                diff_hours = diff.seconds / 3600
                score += diff_hours*25
                score_dict[score] = driver.pk
                score_list.append({score:driver.id})
        for i in sorted (score_dict) :
            drivers.append(Driver.objects.filter(pk=score_dict[i]).as_json())
        return drivers


    def as_json(self):
        return dict(
            latitude=self.latitude,
            longitude=self.longitude,
            rating=self.rating,
            last_trip_time=self.last_trip_time.isoformat())

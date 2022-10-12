from django.db import models
from django.contrib.auth.models import User


class NearBy(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    place_type = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TrainStation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TrainIn(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='trains')
    train_station = models.ForeignKey(TrainStation, on_delete=models.CASCADE, related_name='trainStations')
    fare = models.IntegerField()
    time_table1 = models.CharField(max_length=20)
    time_table2 = models.CharField(max_length=20)

    class Meta:
        ordering = ('train',)

    def __str__(self):
        return '{} at {}'.format(self.train, self.train_station)


class BusStop(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Bus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BusIn(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='buses')
    bus_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name='busStops')
    fare = models.IntegerField()

    class Meta:
        ordering = ('bus',)

    def __str__(self):
        return '{} at {}'.format(self.bus, self.bus_stop)


class CityBusStop(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class CityBus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CityBusIn(models.Model):
    bus = models.ForeignKey(CityBus, on_delete=models.CASCADE, related_name='citybuses')
    bus_stop = models.ForeignKey(CityBusStop, on_delete=models.CASCADE, related_name='citybusstops')
    fare = models.IntegerField()

    class Meta:
        ordering = ('bus',)

    def __str__(self):
        return '{} at {}'.format(self.bus, self.bus_stop)


class Markets(models.Model):
    name = models.CharField(max_length=100)
    market_type = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500)
    average_rating = models.FloatField()
    rating_count = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MarketRatings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    market = models.ForeignKey(Markets, on_delete=models.CASCADE)
    rating = models.FloatField
    comments = models.CharField(max_length=250)


class Services(models.Model):
    TYPE_CHOICES = {('electricity', 'Electricity'), ('plumber', 'Plumber')}
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='Electricity')
    contact = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500)
    average_rating = models.FloatField(default=0)
    rating_count = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name


class Ratings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    rating = models.FloatField
    comments = models.CharField(max_length=250)


class Emergency(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    place_type = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    place_type = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class AddressBook(models.Model):
    name = models.CharField(max_length=500)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class ServiceRatings(models.Model):
    RATING_CHOICES = (
        (1, 1), (2, 2), (3, 3),
        (4, 4), (5, 5)
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return  'rating of {} on {} service'.format(self.user, self.service)


from django.contrib import admin
from .models import Train, TrainStation, TrainIn, Bus, BusStop, BusIn, CityBus, CityBusIn, CityBusStop
from .models import Services

admin.site.register(Train)
admin.site.register(TrainStation)


@admin.register(TrainIn)
class TrainInAdmin(admin.ModelAdmin):
    ordering = ('train_id',)


admin.site.register(Bus)
admin.site.register(BusStop)


@admin.register(BusIn)
class BusInAdmin(admin.ModelAdmin):
    ordering = ('bus_id',)


admin.site.register(CityBus)
admin.site.register(CityBusStop)


@admin.register(CityBusIn)
class CityBusInAdmin(admin.ModelAdmin):
    ordering = ('bus_id',)


admin.site.register(Services)

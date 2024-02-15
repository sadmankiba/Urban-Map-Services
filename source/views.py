from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
from .models import NearBy, Train, TrainIn, TrainStation, Bus, BusIn, BusStop, CityBus, CityBusIn, CityBusStop,\
    AddressBook, Services, ServiceRatings
from .forms import UserRegistrationForm, CityBusForm, InterCityForm, ServiceAddForm, SearchForm, DeleteServiceForm, \
    RateServiceForm
from django.contrib.auth.models import User


@login_required
def dashboard(request):
    city_bus_form = CityBusForm()
    intercity_form = InterCityForm()
    search_form = SearchForm()
    return render(request, 'account/vallagena.html', {'city_bus_form':city_bus_form, 'intercity_form':intercity_form,
                                                      'search_form':search_form})


@login_required
def restaurant_view(request):
    restaurants = NearBy.objects.raw("SELECT * FROM nearby_places(23.727368, 90.38952, 'restaurant')")
    return render(request, 'account/nearby_list.html', {'places': restaurants})


@login_required
def shopping_mall_view(request):
    shopping_malls = NearBy.objects.raw("SELECT * FROM nearby_places(23.727368, 90.38952, 'shopping mall')")
    return render(request, 'account/nearby_list.html', {'places': shopping_malls})


@login_required
def atm_view(request):
    atms = NearBy.objects.raw("SELECT * FROM nearby_places(23.727368, 90.38952, 'atm')")
    return render(request, 'account/nearby_list.html', {'places': atms})


@login_required
def petrol_pump_view(request):
    petrol_pumps = NearBy.objects.raw("SELECT * FROM nearby_places(23.727368, 90.38952, 'petrol pump')")
    return render(request, 'account/nearby_list.html', {'places': petrol_pumps})


@login_required
def pharmacy_view(request):
    pharmacies = NearBy.objects.raw("SELECT * FROM nearby_places(23.727368, 90.38952, 'pharmacy')")
    return render(request, 'account/nearby_list.html', {'places': pharmacies})


@login_required
def bus_stop_view(request):
    bus_stops = NearBy.objects.raw("SELECT * FROM nearby_citybusstops(23.727368, 90.38952)")
    return render(request, 'account/nearby_list.html', {'places': bus_stops})



@login_required
def add_service_view(request):
    added = False
    invalid_form = False
    if request.method == 'POST':
        service_form = ServiceAddForm(request.POST)
        if service_form.is_valid():
            new_service = service_form.save(commit=False)
            new_service.user = request.user
            new_service.save()
            added = True
        else:
            invalid_form = True
    else:
        service_form = ServiceAddForm()

    return render(request, 'account/addService.html',
                  {'service_form':service_form, 'added':added,
                   'invalid_form':invalid_form})


@login_required
def delete_service_view(request):
    deleted = False
    invalid_id = False
    uid = request.user.id
    sql = """
    SELECT * FROM ACCOUNT_SERVICES
    WHERE USER_ID = %s"""
    services = Services.objects.raw(sql, [uid])
    if request.method == "POST":
        form = DeleteServiceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            sql_delete = """
            SELECT * FROM ACCOUNT_SERVICES
            WHERE ID = %s"""
            to_delete_service = Services.objects.raw(sql_delete, [cd['service_id']])
            if to_delete_service.__len__() != 0:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM ACCOUNT_SERVICES WHERE ID = %s", [cd['service_id']])
                deleted = True
            else:
                invalid_id = True
    else:
        form = DeleteServiceForm()

    return render(request, 'account/deleteService.html',
                  {'services':services, 'form':form, 'invalid_id':invalid_id,
                   'deleted':deleted})





@login_required
def search_view(request):
    strr = ""
    if request.method == "POST":
        addr = SearchForm(request.POST)
        if addr.is_valid():
            cd = addr.cleaned_data
            strr = cd['strr']


    pins = AddressBook.objects.raw("SELECT * FROM account_addressbook WHERE strpos(upper(name),upper(%s))>0", [strr])
    return render(request, 'account/search_result.html', {'addresses': pins, 'strr':strr})


@login_required
def search_final_view(request, id):
    addr = AddressBook.objects.raw("SELECT * FROM ACCOUNT_ADDRESSBOOK WHERE ID = %s", [id])
    address = addr[0]
    return render(request, 'account/search_final.html', {'address': address})

################
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user' : new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form' : user_form})


@login_required
def train_view(request):
    submitted = False
    my_zip = ()
    not_found = True
    train_not_found = False
    if request.method == 'POST':
        form = InterCityForm(request.POST)
        if form.is_valid():
            submitted = True
            cd = form.cleaned_data

            origin = cd['origin'].upper()
            destination = cd['destination'].upper()

            sql_id = """
            SELECT * FROM ACCOUNT_TRAINSTATION 
            WHERE UPPER(NAME) = %s"""

            origin_train_station = TrainStation.objects.raw(sql_id, [origin])
            dest_train_station = TrainStation.objects.raw(sql_id, [destination])

            if origin_train_station.__len__() != 0 and dest_train_station.__len__() != 0:
                not_found = False
                origin_id = origin_train_station[0].id
                destination_id = dest_train_station[0].id

                sql_trains = """SELECT T.* 
                        FROM ACCOUNT_TRAININ I JOIN ACCOUNT_TRAIN T
                        ON T.ID = I.TRAIN_ID
                        WHERE I.TRAIN_STATION_ID = %s
                        INTERSECT
                        (
                        SELECT T.* 
                        FROM ACCOUNT_TRAININ I JOIN ACCOUNT_TRAIN T
                        ON T.ID = I.TRAIN_ID
                        WHERE I.TRAIN_STATION_ID = %s
                        );"""

                trains = Train.objects.raw(sql_trains, [origin_id, destination_id])
                if trains.__len__() == 0:
                    train_not_found = True

                sql_fare = """
                SELECT ID, FARE FROM ACCOUNT_TRAININ
                WHERE TRAIN_ID = %s AND TRAIN_STATION_ID = %s"""

                sql_stations1 = """
                SELECT S.ID, S.NAME
                FROM ACCOUNT_TRAININ I JOIN ACCOUNT_TRAINSTATION S 
                ON (I.TRAIN_STATION_ID = S.ID)
                WHERE I.TRAIN_ID = %s AND %s <= I.FARE AND I.FARE <= %s
                ORDER BY I.FARE ASC"""

                sql_stations2 = """
                            SELECT S.ID, S.NAME
                            FROM ACCOUNT_TRAININ I JOIN ACCOUNT_TRAINSTATION S 
                            ON (I.TRAIN_STATION_ID = S.ID)
                            WHERE I.TRAIN_ID = %s AND %s <= I.FARE AND I.FARE <= %s
                            ORDER BY I.FARE DESC"""
                sql_time = """
                SELECT *
                FROM ACCOUNT_TRAININ
                WHERE TRAIN_ID = %s AND TRAIN_STATION_ID = %s
                """

                station_lists = []
                fares = []
                starting_times = []
                arriving_times = []
                for train in trains:
                    origin_fare = TrainIn.objects.raw(sql_fare, [int(train.id), origin_id])
                    dest_fare = TrainIn.objects.raw(sql_fare, [int(train.id), destination_id])
                    fare = dest_fare[0].fare - origin_fare[0].fare
                    starting_time_query = TrainIn.objects.raw(sql_time, [train.id, origin_id])
                    arriving_time_query = TrainIn.objects.raw(sql_time, [train.id, destination_id])
                    if fare < 0:
                        fare = -fare
                        station_list = TrainStation.objects.raw(sql_stations2,
                                                                [train.id, dest_fare[0].fare, origin_fare[0].fare])
                        starting_time = starting_time_query[0].time_table2
                        arriving_time = arriving_time_query[0].time_table2
                    else:
                        station_list = TrainStation.objects.raw(sql_stations1, [train.id, origin_fare[0].fare, dest_fare[0].fare])
                        starting_time = starting_time_query[0].time_table1
                        arriving_time = arriving_time_query[0].time_table1

                    fares.append(fare)
                    starting_times.append(starting_time)
                    arriving_times.append(arriving_time)
                    station_lists.append(station_list)
                my_zip = zip(trains, fares, starting_times, arriving_times, station_lists)
                # t = Train.objects.raw()


    return render(request, 'account/train.html', {'train_not_found': train_not_found,
                  'my_zip': my_zip, 'not_found': not_found, 'submitted': submitted})


@login_required
def bus_view(request):
    submitted = False
    my_zip = ()
    not_found = True
    bus_not_found = False
    buss = []
    fares = []
    stop_lists = []
    if request.method == 'POST':
        form = InterCityForm(request.POST)
        if form.is_valid():
            submitted = True
            cd = form.cleaned_data

            origin = cd['origin'].upper()
            destination = cd['destination'].upper()

            sql_id = """
            SELECT * FROM ACCOUNT_BUSSTOP 
            WHERE UPPER(NAME) = %s"""

            origin_bus_stop = BusStop.objects.raw(sql_id, [origin])
            dest_bus_stop = BusStop.objects.raw(sql_id, [destination])
            if origin_bus_stop.__len__() != 0 and dest_bus_stop.__len__() != 0:
                not_found = False
                origin_id = origin_bus_stop[0].id
                destination_id = dest_bus_stop[0].id

                sql_buss = """SELECT T.* 
                        FROM ACCOUNT_BUSIN I JOIN ACCOUNT_BUS T
                        ON T.ID = I.BUS_ID
                        WHERE I.BUS_STOP_ID = %s
                        INTERSECT
                        (
                        SELECT T.* 
                        FROM ACCOUNT_BUSIN I JOIN ACCOUNT_BUS T
                        ON T.ID = I.BUS_ID
                        WHERE I.BUS_STOP_ID = %s
                        );"""

                buss = Bus.objects.raw(sql_buss, [origin_id, destination_id])
                if buss.__len__() == 0:
                    bus_not_found = True

                sql_fare = """
                SELECT ID, FARE FROM ACCOUNT_BUSIN
                WHERE BUS_ID = %s AND BUS_STOP_ID = %s"""

                sql_stops1 = """
                SELECT S.ID, S.NAME
                FROM ACCOUNT_BUSIN I JOIN ACCOUNT_BUSSTOP S 
                ON (I.BUS_STOP_ID = S.ID)
                WHERE I.BUS_ID = %s AND %s <= I.FARE AND I.FARE <= %s
                ORDER BY I.FARE ASC"""

                sql_stops2 = """
                            SELECT S.ID, S.NAME
                            FROM ACCOUNT_BUSIN I JOIN ACCOUNT_BUSSTOP S 
                            ON (I.BUS_STOP_ID = S.ID)
                            WHERE I.BUS_ID = %s AND %s <= I.FARE AND I.FARE <= %s
                            ORDER BY I.FARE DESC"""
                for bus in buss:
                    origin_fare = BusIn.objects.raw(sql_fare, [int(bus.id), origin_id])
                    dest_fare = BusIn.objects.raw(sql_fare, [int(bus.id), destination_id])
                    fare = dest_fare[0].fare - origin_fare[0].fare

                    if fare < 0:
                        fare = -fare
                        stop_list = BusStop.objects.raw(sql_stops2,
                                                                [bus.id, dest_fare[0].fare, origin_fare[0].fare])

                    else:
                        stop_list = BusStop.objects.raw(sql_stops1, [bus.id, origin_fare[0].fare, dest_fare[0].fare])

                    fares.append(fare)
                    stop_lists.append(stop_list)
                my_zip = zip(buss, fares, stop_lists)


    return render(request, 'account/bus.html', {'buss': buss, 'bus_not_found': bus_not_found,
                  'my_zip':my_zip,'not_found': not_found, 'submitted': submitted})


@login_required
def city_bus_view(request):
    submitted = False
    my_zip = ()
    not_found = True
    bus_not_found = False
    bus_list = []
    fares = []
    stop_lists = []
    if request.method == 'POST':
        form = CityBusForm(request.POST)
        if form.is_valid():
            submitted = True
            cd = form.cleaned_data

            origin = cd['origin'].upper()
            destination = cd['destination'].upper()

            sql_id = """
            SELECT * FROM ACCOUNT_CITYBUSSTOP 
            WHERE UPPER(NAME) = %s"""

            origin_bus_stop = CityBusStop.objects.raw(sql_id, [origin])
            dest_bus_stop = CityBusStop.objects.raw(sql_id, [destination])
            if origin_bus_stop.__len__() != 0 and dest_bus_stop.__len__() != 0:
                not_found = False
                origin_id = origin_bus_stop[0].id
                destination_id = dest_bus_stop[0].id

                sql_buss = """SELECT T.* 
                        FROM ACCOUNT_CITYBUSIN I JOIN ACCOUNT_CITYBUS T
                        ON T.ID = I.BUS_ID
                        WHERE I.BUS_STOP_ID = %s
                        INTERSECT
                        (
                        SELECT T.* 
                        FROM ACCOUNT_CITYBUSIN I JOIN ACCOUNT_CITYBUS T
                        ON T.ID = I.BUS_ID
                        WHERE I.BUS_STOP_ID = %s
                        );"""

                bus_list = CityBus.objects.raw(sql_buss, [origin_id, destination_id])
                if bus_list.__len__() == 0:
                    bus_not_found = True

                sql_fare = """
                SELECT ID, FARE FROM ACCOUNT_CITYBUSIN
                WHERE BUS_ID = %s AND BUS_STOP_ID = %s"""

                sql_stops1 = """
                SELECT S.ID, S.NAME
                FROM ACCOUNT_CITYBUSIN I JOIN ACCOUNT_CITYBUSSTOP S 
                ON (I.BUS_STOP_ID = S.ID)
                WHERE I.BUS_ID = %s AND %s <= I.FARE AND I.FARE <= %s
                ORDER BY I.FARE ASC"""

                sql_stops2 = """
                            SELECT S.ID, S.NAME
                            FROM ACCOUNT_CITYBUSIN I JOIN ACCOUNT_CITYBUSSTOP S 
                            ON (I.BUS_STOP_ID = S.ID)
                            WHERE I.BUS_ID = %s AND %s <= I.FARE AND I.FARE <= %s
                            ORDER BY I.FARE DESC"""
                for bus in bus_list:
                    origin_fare = CityBusIn.objects.raw(sql_fare, [int(bus.id), origin_id])
                    dest_fare = CityBusIn.objects.raw(sql_fare, [int(bus.id), destination_id])
                    fare = dest_fare[0].fare - origin_fare[0].fare

                    if fare < 0:
                        fare = -fare
                        stop_list = CityBusStop.objects.raw(sql_stops2,
                                                            [bus.id, dest_fare[0].fare, origin_fare[0].fare])

                    else:
                        stop_list = CityBusStop.objects.raw(sql_stops1,
                                                            [bus.id, origin_fare[0].fare, dest_fare[0].fare])

                    fares.append(fare)
                    stop_lists.append(stop_list)
                my_zip = zip(bus_list, fares, stop_lists)
                submitted = True
    else:
        not_found = True

    return render(request, 'account/city_bus.html', {'bus_list': bus_list, 'bus_not_found': bus_not_found,
                  'my_zip': my_zip, 'not_found': not_found, 'submitted': submitted})


@login_required
def service_detail_view(request, sid):
    services = Services.objects.raw("SELECT * FROM ACCOUNT_SERVICES WHERE ID = %s", [sid])
    provider = ""
    sql = """SELECT * FROM ACCOUNT_SERVICERATINGS
                    WHERE USER_ID = %s AND SERVICE_ID = %s"""
    if services.__len__() == 0:
        service = []
        service_not_found = True
        form = RateServiceForm()
    else:
        service = services[0]
        sql_uid = """SELECT * FROM ACCOUNT_SERVICES
        WHERE ID = %s"""
        uid_row = Services.objects.raw(sql_uid, [sid])
        uid = uid_row[0]
        sql_provider = """SELECT * 
        FROM AUTH_USER
        WHERE ID = %s"""
        service_not_found = False
        provider_row = User.objects.raw(sql_provider, [uid.user_id])
        if provider_row.__len__() != 0:
            provider = provider_row[0].first_name + " " + provider_row[0].last_name
        if request.method == "POST":
            form = RateServiceForm(data=request.POST)
            if form.is_valid():
                cur_rating = ServiceRatings.objects.raw(sql, [request.user.id, sid])
                if cur_rating.__len__() == 0:
                    new_rating = form.save(commit=False)
                    new_rating.user = request.user
                    new_rating.service = service
                    new_rating.save()
                else:
                    new_rating = form.save(commit=False)
                    cur_rating[0].rating = new_rating.rating
                    cur_rating[0].save()

    rating = ServiceRatings.objects.raw(sql, [request.user.id, sid])
    if rating.__len__() == 0:
        user_rating = 0
    else:
        user_rating = rating[0].rating
    if request.method == "GET":
        form = RateServiceForm()

    return render(request, 'account/serviceDetail.html',
                  {'service':service, 'service_not_found':service_not_found,
                   'form':form, 'user_rating':user_rating, 'provider':provider})









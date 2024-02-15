from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Services, Markets, Emergency, Hospital


@login_required
def electricity_view(request):
    electricians = Services.objects.raw("SELECT * FROM nearby_services(23.727368, 90.38952, 'electricity')")
    return render(request, 'account/nearby_services_list.html', {'services': electricians})


@login_required
def plumber_view(request):
    plumbers = Services.objects.raw("SELECT * FROM nearby_services(23.727368, 90.38952, 'plumber')")
    return render(request, 'account/nearby_services_list.html', {'services': plumbers})


@login_required
def chicken_view(request):
    chickens = Markets.objects.raw("SELECT * FROM nearby_markets(23.727368, 90.38952, 'chicken')")
    return render(request, 'account/nearby_market_list.html', {'markets': chickens})


@login_required
def meat_view(request):
    meats = Markets.objects.raw("SELECT * FROM nearby_markets(23.727368, 90.38952, 'meat')")
    return render(request, 'account/nearby_market_list.html', {'markets': meats})


@login_required
def police_view(request):
    polices = Emergency.objects.raw("SELECT * FROM nearby_emergencies(23.727368, 90.38952, 'police')")
    return render(request, 'account/nearby_emergency_list.html', {'emergencies': polices})


@login_required
def fire_service_view(request):
    fire_services = Emergency.objects.raw("SELECT * FROM nearby_emergencies(23.727368, 90.38952, 'fire service')")
    return render(request, 'account/nearby_emergency_list.html', {'emergencies': fire_services})


@login_required
def medical_center_view(request):
    medical_centers = Hospital.objects.raw("SELECT * FROM nearby_hospitals(23.727368, 90.38952, 'medical center')")
    return render(request, 'account/nearby_hospital_list.html', {'hospitals': medical_centers})


@login_required
def diagnostics_view(request):
    diagnostics = Hospital.objects.raw("SELECT * FROM nearby_hospitals(23.727368, 90.38952, 'diagnostics')")
    return render(request, 'account/nearby_hospital_list.html', {'hospitals': diagnostics})


@login_required
def ratings_view(request, service_provider_id):
    service_provider = Services.objects.raw("SELECT * FROM account_services WHERE id = %s", [service_provider_id])
    return render(request, 'account/rating_page.html', {'service_provider': service_provider})




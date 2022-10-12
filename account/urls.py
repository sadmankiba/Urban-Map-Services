from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, views2


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('restaurant/', views.restaurant_view, name='restaurant_view'),
    path('shopping_malls/', views.shopping_mall_view, name='shopping_mall_view'),
    path('petrol_pump/', views.petrol_pump_view, name='petrol_pump_view'),
    path('atm/', views.atm_view, name='atm_view'),
    path('pharmacy/', views.pharmacy_view, name='pharmacy_view'),
    path('bus_stops/', views.bus_stop_view, name='bus_stop_view'),
    path('add_service/', views.add_service_view, name='add_service_view'),
    path('delete_service/', views.delete_service_view, name='delete_service_view'),
    path('register/', views.register, name='register'),
    path('train/', views.train_view, name='train_view'),
    path('bus/', views.bus_view, name='bus_view'),
    path('city_bus/', views.city_bus_view, name='city_bus_view'),
    #path('services/<int:sid>/', views.service_detail_view, name='service_detail_view'),


    path('search_results/', views.search_view, name='search_view'),
    path('search_final/<int:id>', views.search_final_view, name='search_final_view'),


    ##############


    path('electricians/', views2.electricity_view, name='electricity_view'),
    path('plumbers/', views2.plumber_view, name='plumber_view'),
    path('chicken/', views2.chicken_view, name='chicken_view'),
    path('meat/', views2.meat_view, name='meat_view'),

    path('police/', views2.police_view, name='police_view'),
    path('fire_service/', views2.fire_service_view, name='fire_service_view'),
    path('medical_center/', views2.medical_center_view, name='medical_center_view'),
    path('diagnostics/', views2.diagnostics_view, name='diagnostics_view'),
    path('ratings/<int:sid>/', views.service_detail_view, name='service_detail_view'),

]

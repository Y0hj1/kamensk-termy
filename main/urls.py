from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),

    # Услуги
    path('services/termalnye-basseyny/', views.services_thermal_pools, name='thermal_pools'),
    path('services/bani/', views.services_baths, name='baths'),
    path('services/zona-spa/spa/', views.services_spa, name='spa'),
    path('services/eda/', views.services_cafe, name='cafe'),
    path('services/detyam/', views.services_children, name='children'),
    path('services/otel/', views.services_hotel, name='hotel'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),

    # Остальные страницы
    path('price/', views.price_list, name='price'),
    path('actions/', views.actions, name='actions'),
    path('projects/', views.gallery, name='gallery'),
    path('contacts/', views.contacts, name='contacts'),
    path('gift-certificates/', views.certificates, name='certificates'),
    path("contacts/", views.contacts, name="contacts"),

]

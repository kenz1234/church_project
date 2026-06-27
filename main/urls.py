from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('events/', views.events, name='events'),
    path('donate/', views.donate, name='donate'),
    path('prayerrequest/', views.prayer_request, name='prayer_request'),
    path('queries/', views.queries, name='queries'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trips/create/', views.create_trip, name='create_trip'),
    path('trips/my/', views.my_trips, name='my_trips'),
    path('trips/<int:trip_id>/edit/', views.edit_trip, name='edit_trip'),
    path('trips/<int:trip_id>/delete/', views.delete_trip, name='delete_trip'),
    path('requests/create/', views.create_request, name='create_request'),
    path('requests/my/', views.my_requests, name='my_requests'),
    path('requests/<int:request_id>/delete/', views.delete_request, name='delete_request'),
] 
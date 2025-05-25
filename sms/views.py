from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Trip, Request

def home(request):
    trips = Trip.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'trips': trips})

def create_trip(request):
    if request.method == 'POST':
        start_location = request.POST.get('start_location', '')
        end_location = request.POST.get('end_location', '')
        date = request.POST.get('date', '')
        seats = request.POST.get('seats', '')
        description = request.POST.get('description', '')
        
        if not all([start_location, end_location, date, seats, description]):
            messages.error(request, 'All fields are required')
            return render(request, 'create_trip.html')
            
        try:
            seats = int(seats)
            if seats < 1:
                messages.error(request, 'Seats must be a positive number')
                return render(request, 'create_trip.html')
        except ValueError:
            messages.error(request, 'Seats must be a number')
            return render(request, 'create_trip.html')
            
        try:
            date = timezone.make_aware(timezone.datetime.strptime(date, '%Y-%m-%dT%H:%M'))
            
            trip = Trip(
                user=None,
                start_location=start_location,
                end_location=end_location,
                date=date,
                seats=seats,
                description=description
            )
            trip.save()
            messages.success(request, 'Trip created successfully')
            return redirect('home')
        except:
            messages.error(request, 'Error creating trip')
            return render(request, 'create_trip.html')

    return render(request, 'create_trip.html')

def my_trips(request):
    trips = Trip.objects.all().order_by('-created_at')
    return render(request, 'my_trips.html', {'trips': trips})

def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    try:
        trip.delete()
        messages.success(request, 'Trip deleted successfully')
    except:
        messages.error(request, 'Error deleting trip')
    return redirect('my_trips')

def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    
    if request.method == 'POST':
        start_location = request.POST.get('start_location', '')
        end_location = request.POST.get('end_location', '')
        date = request.POST.get('date', '')
        seats = request.POST.get('seats', '')
        description = request.POST.get('description', '')
        
        if not all([start_location, end_location, date, seats, description]):
            messages.error(request, 'All fields are required')
            return render(request, 'edit_trip.html', {'trip': trip})
            
        try:
            seats = int(seats)
            if seats < 1:
                messages.error(request, 'Seats must be a positive number')
                return render(request, 'edit_trip.html', {'trip': trip})
        except ValueError:
            messages.error(request, 'Seats must be a number')
            return render(request, 'edit_trip.html', {'trip': trip})
            
        try:
            date = timezone.make_aware(timezone.datetime.strptime(date, '%Y-%m-%dT%H:%M'))
            
            trip.start_location = start_location
            trip.end_location = end_location
            trip.date = date
            trip.seats = seats
            trip.description = description
            trip.save()
            messages.success(request, 'Trip updated successfully')
            return redirect('my_trips')
        except:
            messages.error(request, 'Error updating trip')
            return render(request, 'edit_trip.html', {'trip': trip})
            
    return render(request, 'edit_trip.html', {'trip': trip})

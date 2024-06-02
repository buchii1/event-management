from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import timedelta
from django.utils import timezone
from django.db import IntegrityError
from django.http import HttpResponse

import requests
from ics import Calendar, Event as IcsEvent

from .models import Event, Booking, Organizer
from .forms import EventForm, OrganizerForm
from .utils import calculate_time_to_event

userModel = get_user_model()


def index(request):
    """
    Render the events home page.
    Args:
        request: The HTTP request object.    
    Returns:
        HttpResponse: The rendered HTML for the home page.
    """
    return render(request, 'main/index.html')

@login_required
def add_event(request):
    """
    Handle the event addition form for superusers.
    Args:
        request: The HTTP request object.
    Returns:
        HttpResponse: The event form page or redirects to the index page.
    """
    user = request.user
    add_event = True

    if user.is_superuser:
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, ("Event was added successfully!"))
                return redirect('main:events')
        else:
            form = EventForm()
            context = {
                'form': form,
                'add_event': add_event,
            }
        return render(request, 'main/event_form.html', context)
    else:
        return redirect('main:index')
    

@login_required
def edit_event(request, event_title):
    """
    Edit an existing event for superusers.
    Args:
        request: The HTTP request object.
        event_title: The title of the event to be edited.
    Returns:
        HttpResponse: The event form page or redirects to the index page.
    """
    event = get_object_or_404(Event, title=event_title)
    user = request.user
    add_event = False

    if user.is_superuser:
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                form.save()
                messages.success(request, ("Event was updated successfully!"))
                return redirect('main:event_detail', event_title=event.title)
        else:
            form = EventForm(instance=event)
            context = {
                'event': event,
                'form': form,
                'add_event': add_event,
            }
        return render(request, 'main/event_form.html', context)
    else:
        return redirect('main:index')
    

@login_required
def delete_event(request, event_pk):
    """
    Delete an existing event.
    Args:
        request: The HTTP request object.
        event_pk: The primary key of the event to be deleted.
    Returns:
        HttpResponse: Redirects to the events page.
    """
    event = get_object_or_404(Event, pk=event_pk)
    event.delete()
    return redirect('main:events')


def events(request):
    """
    Display a paginated list of events.
    Args:
        request: The HTTP request object.
    Returns:
        HttpResponse: The events page with a list of events.
    """
    events = Event.objects.all()
    paginator = Paginator(events, 5)
    page = request.GET.get('page')
    
    try:
        events_page = paginator.page(page)
    except PageNotAnInteger:
        events_page = paginator.page(1)
    except EmptyPage:
        events_page = paginator.page(paginator.num_pages)
    
    return render(request, 'main/events.html', {'events': events_page})


def event_detail(request, event_title):
    """
    Display the details of a specific event.
    Args:
        request: The HTTP request object.
        event_title: The title of the event to be displayed.
    Returns:
        HttpResponse: The event detail page.
    """
    event = get_object_or_404(Event, title=event_title)
    # Initialize user_bookings to None 
    # if the user is not authenticated
    user_bookings = Booking.objects.none()
    
    if request.user.is_authenticated:
        user_bookings = Booking.objects.filter(user=request.user, event=event)

    slots_left = event.capacity - event.attendees_count
    time_to_event = calculate_time_to_event(event.start_date)
    today = timezone.now().date()
    context = {
        'event': event,
        'slots_left': slots_left,
        'time_to_event': time_to_event,
        'today': today,
        'user_bookings': user_bookings
    }
    return render(request, 'main/event_detail.html', context)  


@login_required
def book_event(request, event_id):
    """
    Book a spot for a specific event.
    Args:
        request: The HTTP request object.
        event_id: The primary key of the event to be booked.
    Returns:
        HttpResponse: Redirects to the event detail page.
    """
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        user = request.user
        try:
            Booking.create_booking(user, event)
            messages.success(request, "Booking successfully reserved!")
            return redirect('main:event_detail', event_title=event.title)
        except IntegrityError:
            # If IntegrityError occurs (user has already booked the event),
            # display an appropriate error message
            messages.error(request, "You have already booked this event.")
            return redirect('main:event_detail', event_title=event.title)
        

@login_required
def add_organizer(request):
    """
    Add a new organizer.
    Args:
        request: The HTTP request object.
    Returns:
        HttpResponse: The organizer form page or redirects to the index page.
    """
    user = request.user
    add_organizer = True

    if user.is_superuser:
        if request.method == 'POST':
            form = OrganizerForm(request.POST, request.FILES)
            if form.is_valid():
                organizer_name = form.cleaned_data['name']
                form.save()
                messages.success(request, (f"<b>{organizer_name}</b> was added successfully!"))
                return redirect('main:index')
        else:
            form = OrganizerForm()
            context = {
                'form': form,
                'add_organizer': add_organizer
            }
        return render(request, 'main/organizer_form.html', context)
    else:
        return redirect('main:index')
    

def organizer(request, name):
    """
    Display the details of a specific organizer.
    Args:
        request: The HTTP request object.
        name: The name of the organizer.
    Returns:
        HttpResponse: The organizer detail page.
    """
    organizer = get_object_or_404(Organizer, name=name)
    return render(request, 'main/organizer.html', {'organizer': organizer})
        

@login_required
def profile(request, username):
    """
    Display the profile and bookings of a specific user.
    Args:
        request: The HTTP request object.
        username: The username of the user.
    Returns:
        HttpResponse: The profile page.
    """
    user = get_object_or_404(userModel, username=username)
    bookings = Booking.objects.filter(user=user).select_related('event')

    paginator = Paginator(bookings, 6)
    page = request.GET.get('page')
    
    try:
        user_bookings = paginator.page(page)
    except PageNotAnInteger:
        user_bookings = paginator.page(1)
    except EmptyPage:
        user_bookings = paginator.page(paginator.num_pages)
    context = {
        'user': user,
        'user_bookings': user_bookings
    }
    return render(request, 'main/profile.html', context)


def fetch_qr_code(request, booking_id):
    """
    Fetch a QR code for a specific booking.
    Args:
        request: The HTTP request object.
        booking_id: The ID of the booking.
    Returns:
        HttpResponse: The QR code image.
    """
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?data={booking_id}"
    response = requests.get(qr_code_url)

    # Return the image data as the HTTP response
    return HttpResponse(response.content, content_type="image/png")


def download_event_ics(request, event_id):
    """
    Generate and download an iCalendar (.ics) file for the specified event.
    Parameters:
        request (HttpRequest): The HTTP request object.
        event_id (int): The ID of the event to download.
    Returns:
        HttpResponse: The generated .ics file.
    """
    event = get_object_or_404(Event, pk=event_id)
    # Manually adjust the time offset (temporary fix)
    event_start = event.start_date - timedelta(hours=1)
    event_end = event.end_date - timedelta(hours=1)

    calendar = Calendar()
    event_ics = IcsEvent()

    event_ics.name = event.title
    event_ics.begin = event_start.isoformat()
    event_ics.end = event_end.isoformat()
    event_ics.location = event.venue
    event_ics.description = ' '.join(event.description.split()[:20])

    calendar.events.add(event_ics)

    response = HttpResponse(content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename="{event.title}.ics"'
    response.write(calendar.serialize())
    return response

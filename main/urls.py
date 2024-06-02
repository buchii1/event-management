from django.urls import path

from .views import *
app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('add-event/', add_event, name='addEvent'),
    path('add-organizer/', add_organizer, name="add_organizer"),
    path('events/', events, name='events'),
    path('event/<str:event_title>/', event_detail, name="event_detail"),
    path('event/<int:event_id>/book/', book_event, name="book_event"),
    path('edit/<str:event_title>/', edit_event, name='edit_event'),
    path('delete/<int:event_pk>/', delete_event, name='delete_event'),
    path('user/<str:username>/', profile, name='profile'),
    path('organizer/<str:name>/', organizer, name='organizer'),
    path('fetch-qr-code/<int:booking_id>/', fetch_qr_code, name='fetch_qr_code'),
    path('download_event_ics/<int:event_id>/', download_event_ics, name='download_event_ics'),
]

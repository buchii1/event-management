from django.contrib import admin

from .models import Event, Booking, Organizer

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin view for Event Model"""
    list_display = ('title', 'venue', 'reg_deadline', 'start_date')
    ordering = ('-start_date',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin view for Booking Model"""
    list_display = ('user', 'event', 'created_at')
    readonly_fields = ('booking_id',)
    ordering = ('-created_at',)


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    """Admin view for Organizer Model"""
    list_display = ('name', 'email', 'title', 'address')
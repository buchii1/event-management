from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import random, string

userModel = get_user_model()

# Create your models here.
class Event(models.Model):
    """Model for representing an event."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reg_deadline = models.DateField()
    venue = models.CharField(max_length=80)
    capacity = models.PositiveIntegerField()
    attendees_count = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(default='event_images/default.webp', upload_to="event_images")
    image = models.ImageField(default='event_images/event.jpg', upload_to="event_images")
    organizers = models.ManyToManyField("Organizer", related_name='organizers')

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['start_date']
        

class Booking(models.Model):
    """Model for representing a booking."""
    user = models.ForeignKey(userModel, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=8, unique=True, default=None, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Enforce uniqueness of user-event pairs
        unique_together = ('user', 'event')
        ordering = ['event__start_date']

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

    def clean(self):
        """Validate uniqueness of user-event pairs."""
        super().clean()
        if Booking.objects.filter(user=self.user, event=self.event).exists():
            raise ValidationError("You have already booked this event.")

    def generate_booking_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    @classmethod
    def create_booking(cls, user, event):
        """Create a booking for the user and event."""
        booking_id = cls().generate_booking_id()
        if event.attendees_count < event.capacity:
            booking = cls.objects.create(user=user, event=event, booking_id=booking_id)
            event.attendees_count += 1
            event.save()
            return booking
        else:
            raise ValidationError({'event': _(f"Event is fully booked.")})
    

class Organizer(models.Model):
    """Model for representing an organizer."""
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=30, unique=True)
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(default='organizer_images/organizer.jpg', upload_to="organizer_images")

    def __str__(self):
        return self.name

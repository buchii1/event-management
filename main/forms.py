from django import forms

from .models import Event, Organizer


class EventForm(forms.ModelForm):
    """
    New Event Form
    """
    organizers = forms.ModelMultipleChoiceField(queryset=Organizer.objects.all(),
        widget=forms.SelectMultiple(attrs={'id': 'organizers', 
            'data-placeholder': 'Select organizers...'}))

    class Meta:
        model = Event
        exclude = ['attendees_count']
        widgets = {
            'reg_deadline': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 7}),
        }


class OrganizerForm(forms.ModelForm):
    """
    New Organizer Form
    """

    class Meta:
        model = Organizer
        fields = '__all__'
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
        }
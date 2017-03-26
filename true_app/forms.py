
from django import forms
from true_app.models import Event


class CreateEventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'start_date', 'num_months_between_occ',
                  'day_of_month_of_occ', 'num_days_offset')


import datetime

import holidays
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, DeleteView, \
    ListView, UpdateView

from true_app.forms import CreateEventForm
from true_app.models import Event


class CreateEvent(CreateView):
    model = Event
    template_name = 'create_event.html'
    form_class = CreateEventForm


class EventUpdate(UpdateView):
    model = Event
    form_class = CreateEventForm
    template_name = 'event_update_form.html'
    pk_url_kwarg = 'event_id'


class EventDetail(DetailView):
    model = Event
    template_name = 'event_detail.html'
    pk_url_kwarg = 'event_id'

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        """ add next four deliveries to the detail page """
        event = Event.objects.get(pk=self.kwargs.get('event_id', None))
        deliveries = []
        for i in range(4):
            next_day = event.delivery_date.day
            next_year = event.delivery_date.year
            next_month = (event.delivery_date.month +
                          i * event.num_months_between_occ) % 12
            if (event.delivery_date.month +
                          i * event.num_months_between_occ) > 12:
                next_year +=1

            created = False
            while not created:
                # handle days that don't exist in the month
                try:
                    next_date = datetime.date(day=next_day,
                                              year=next_year,
                                              month=next_month if next_month > 0 else 12)
                    created = True
                except ValueError:
                    next_day -= 1

            # make sure this date is not a holiday or weekend before adding it
            next_date = self.valid_delivery_date(next_date)

            deliveries.append(next_date)
        context['deliveries'] = deliveries
        return context

    @staticmethod
    def valid_delivery_date(delivery_date):
        us_holidays = holidays.UnitedStates()
        while delivery_date.weekday() > 4 or delivery_date in us_holidays:
            delivery_date = delivery_date - datetime.timedelta(days=1)

        return delivery_date


class AllEvents(ListView):
    model = Event
    template_name = 'event_list.html'


class DeleteEvent(DeleteView):
    model = Event
    template_name = 'event_confirm_delete.html'
    pk_url_kwarg = 'event_id'

    def get_success_url(self):
        return reverse('event_list')

import datetime

from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView

from true_app.forms import CreateEventForm
from true_app.models import Event


class CreateEvent(CreateView):
    model = Event
    template_name = 'create_event.html'
    form_class = CreateEventForm


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
            print(event.delivery_date)
            print(event.delivery_date.month + i)
            next_date = datetime.date(day=event.delivery_date.day,
                                      year=event.delivery_date.year,
                                      month=event.delivery_date.month + i)
            deliveries.append(next_date)
        context['deliveries'] = deliveries
        return context


class DeleteEvent(DeleteView):
    model = Event
    success_url = reverse_lazy('event-list')
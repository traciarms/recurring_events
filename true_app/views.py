from django.shortcuts import render
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
        deliveries = []

        return context

class DeleteEvent(DeleteView):
    model = Event
    success_url = reverse_lazy('event-list')
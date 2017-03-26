import datetime
import unittest

from django.test import TestCase

from django.urls import reverse

from true_app.models import Event
from true_app.views import EventDetail, AllEvents
from django.test import RequestFactory


class EventViewTests(TestCase):
    def test_event_detail_404(self):
        url = reverse('detail', args=[100])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404, msg='not found')

    def test_event_detail(self):
        test_event = Event.objects.create(name='test',
                                          start_date=datetime.date(day=12,
                                                                   month=12,
                                                                   year=2017),
                                          )
        test_event.save()

        response = self.client.get(reverse('detail', args=[test_event.id]))
        self.assertEqual(response.status_code, 200, msg='found page')

    def test_event_list(self):
        test_event = Event.objects.create(name='test',
                                          start_date=datetime.date(day=12,
                                                                   month=12,
                                                                   year=2017),
                                          )
        test_event.save()

        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200, msg='found page')

    def test_event_update(self):
        test_event = Event.objects.create(name='test',
                                          start_date=datetime.date(day=12,
                                                                   month=12,
                                                                   year=2017),
                                          )
        test_event.save()

        response = self.client.get(reverse('update', args=[test_event.id]))
        self.assertEqual(response.status_code, 200, msg='found page')


class EventSaveTest(TestCase):

    def test_event_save_same_month_weekend(self):
        test_event = Event.objects.create(name='test',
                                          start_date=datetime.date(day=12,
                                                                   month=12,
                                                                   year=2017),
                                          num_months_between_occ=1,
                                          day_of_month_of_occ=30,
                                          num_days_offset=1
                                          )
        test_event.save()
        self.assertTrue(test_event.delivery_date ==
                        datetime.date(day=29,
                                      month=12,
                                      year=2017))

    def test_event_save_next_month(self):
        test_event = Event.objects.create(name='test',
                                          start_date=datetime.date(day=31,
                                                                   month=12,
                                                                   year=2017),
                                          num_months_between_occ=1,
                                          day_of_month_of_occ=30,
                                          num_days_offset=1
                                          )
        test_event.save()
        self.assertTrue(test_event.delivery_date ==
                        datetime.date(day=30,
                                      month=1,
                                      year=2018))

    def test_event_save_next_month_weekend(self):
        test_event = Event.objects.create(name='test',
                                          start_date=datetime.date(day=28,
                                                                   month=12,
                                                                   year=2017),
                                          num_months_between_occ=1,
                                          day_of_month_of_occ=27,
                                          num_days_offset=1
                                          )
        test_event.save()
        self.assertTrue(test_event.delivery_date ==
                        datetime.date(day=26,
                                      month=1,
                                      year=2018))


class EventViewTestCase(unittest.TestCase):
    def test_get(self):
        # Setup name.
        name = 'test event'
        # Setup request and view.
        request = RequestFactory().get('/fake-path')
        view = AllEvents.as_view(template_name='event_list.html')
        # Run.
        response = view(request, name=name)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'event_list.html')

from django.test import TestCase

from django.urls import reverse

from true_app.models import Event


class CreateEventTests(TestCase):
    def test_create_event_404(self):
        test_event = Event.objects.create('name', '12-12-2017', 1, 1, 1)
        test_event.save()

        url = reverse('detail', args=[100])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404, msg='not found')

    def test_create_event(self):
        test_event = Event.objects.create('name', '12-12-2017', 1, 1, 1)
        test_event.save()
        event = Event.objects.\
            create(name='name', start_date='12-12-2017',
                   num_months_between_occ=1,
                   day_of_month_of_occ=1,
                   num_days_offset=1)
        event.save()

        response = self.client.get(reverse('detail'))
        self.assertEqual(response.status_code, 200, msg='found page')
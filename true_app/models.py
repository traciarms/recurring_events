from __future__ import unicode_literals

import datetime
import holidays
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.urls import reverse


class Event(models.Model):
    name = models.CharField(max_length=250, unique=True)
    start_date = models.DateField()
    num_months_between_occ = models.IntegerField(default=1, validators=[
                                            MinValueValidator(1)
                                        ])
    day_of_month_of_occ = models.IntegerField(default=1, validators=[
                                            MaxValueValidator(31),
                                            MinValueValidator(1)
                                        ])
    num_days_offset = models.IntegerField(default=1, validators=[
                                            MinValueValidator(1)
                                        ])
    calculated_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        today = datetime.datetime.now()
        month = today.month
        year = today.year

        # first calculate the calculated date from the day of month given
        self.calculated_date = datetime.date(day=self.day_of_month_of_occ,
                                             year=year,
                                             month=month)
        while self.calculated_date < self.start_date:
            next_day = self.day_of_month_of_occ
            next_year = year
            next_month = (self.calculated_date.month + 1) % 12
            if (self.calculated_date.month + 1) > 12:
                next_year += 1

            created = False
            while not created:
                # handle days that don't exist in the month
                try:
                    self.calculated_date = datetime.date(day=next_day,
                                                         year=next_year,
                                                         month=next_month if next_month > 0 else 12)
                    created = True
                except ValueError:
                    next_day -= 1

        self.delivery_date = self.calculated_date

        us_holidays = holidays.UnitedStates()
        while self.delivery_date.weekday() > 4 or \
                self.delivery_date in us_holidays:
            self.delivery_date = self.delivery_date - datetime.timedelta(days=1)

            # make sure we have not gone back past the start date - if so
            # go forward to the next month
            if self.delivery_date < self.start_date:
                next_day = self.day_of_month_of_occ
                next_year = self.delivery_date.year
                next_month = (self.delivery_date.month + 1) % 12
                if (self.delivery_date.month + 1) > 12:
                    next_year += 1

                created = False
                while not created:
                    try:
                        self.day_of_month_of_occ = \
                            datetime.date(day=next_day,
                                          year=next_year,
                                          month=next_month)
                    except ValueError:
                        next_day -= 1

        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'event_id': self.pk})
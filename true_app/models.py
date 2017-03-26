from __future__ import unicode_literals

from datetime import datetime, date

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

        start_date = self.start_date
        self.calculated_date = \
            date(day=self.day_of_month_of_occ, year=year, month=month)
        if self.calculated_date < start_date:
            self.calculated_date = \
                date(day=self.day_of_month_of_occ, year=year, month=month+1)


        # if self.day_of_month_of_occ
        # self.calculated_date =
        #
        # to_date = from_date
        # while number_of_days:
        #     to_date += timedelta(1)
        #     if to_date.weekday() < 5:  # i.e. is not saturday or sunday
        #         number_of_days -= 1
        # return to_date
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'event_id': self.pk})
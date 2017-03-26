## Description

The user is able to Create Events, Update Events, List All Events and Delete
Events.

## Details

The delivery date is calculated based on the given start date, and avoiding
any weekends or holidays.  If by avoiding weekends or holidays the deliver_date
if found to be prior to the start date, the deliver date will be advanced to
the following month.

The Event detail page lists the event and the next 4 upcoming deliveries.
This method calculates those next deliveries using the number of months
between deliveries and watches for end of month, end of year and any days that
are out of range for the month.  In other words it shouldn't produce any
weekend or holiday days or invalid days.

I wasn't sure how to use the number of days offset, so I don't think I used
it in any of the calculations.  The user can enter it and it is being stored
with the event, but again, I didn't see how to use it in the calculations.

### Deliverables

* A zip file from the GitHub repo

### Execute

* To run first:
 pip install requirments.txt
./manage.py runserver
visit the link http://127.0.0.1:8000/ to create an event
visit http://127.0.0.1:8000/all to view all events and then subsequently edit
and delete events.



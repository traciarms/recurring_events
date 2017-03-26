from django.conf.urls import url

from true_app.views import CreateEvent, EventDetail, AllEvents, EventUpdate, \
    DeleteEvent

urlpatterns = [
    #
    url(r'^all/', AllEvents.as_view(), name='event_list'),

    url(r'^detail/(?P<event_id>[\d]+)', EventDetail.as_view(),
        name='detail'),
    url(r'^update/(?P<event_id>[\d]+)', EventUpdate.as_view(),
        name='update'),
    url(r'^delete/(?P<event_id>[\d]+)', DeleteEvent.as_view(),
        name='delete'),

    url(r'^$', CreateEvent.as_view(), name='create'),

]
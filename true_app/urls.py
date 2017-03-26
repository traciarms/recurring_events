from django.conf.urls import url

from true_app.views import CreateEvent, EventDetail

urlpatterns = [
    #
    # url(r'^all/', AllEvents.as_view(), name='show_all'),

    url(r'^detail/(?P<event_id>[\d]+)', EventDetail.as_view(),
        name='detail'),
    # url(r'^update/(?P<event_id>[\d]+)', EventUpdate.as_view(),
    #     name='update'),

    url(r'^$', CreateEvent.as_view(), name='create'),

]
#Url Conf
#Namespace: scraper
from django.conf.urls import url
from scraper.views import Index, Scraper, Add_Series, Tracker, Delete_Series, \
                          Update_Series, Search_Series, Latest_Movies

urlpatterns = [
    url(r'^$', Index.as_view(), name = 'index'),

    url(r'^scrape/$', Scraper.as_view(), name = 'scrape'),
    url(r'^scrape/add/$', Add_Series.as_view(), name = 'add_series'),

    url(r'^tracker/$', Tracker.as_view(), name = 'tracker'),
    url(r'^tracker/search/$', Search_Series.as_view(), name = 'search'),
    url(r'^tracker/remove/(?P<pk>[0-9]+)/$', Delete_Series.as_view(), name = 'remove_series'),
    url(r'^tracker/update/(?P<pk>[0-9]+)/$', Update_Series.as_view(), name = 'update_series'),

    url(r'^latest_movies/$', Latest_Movies.as_view(), name = 'latest_movies'),
]

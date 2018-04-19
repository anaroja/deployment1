from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
    # url(r'^reset$', views.reset),
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$', views.home),
    url(r'^create$', views.create),
    url(r'^add_quote/(?P<quote_id>\d+)$', views.add_quote),
    url(r'^display_quote/(?P<created_by_id>\d+)$', views.display_quote),
    url(r'^remove/(?P<quote_id>\d+)$', views.remove),
    url(r'^logout$', views.logout),
]

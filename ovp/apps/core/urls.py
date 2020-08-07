from django.conf.urls import url, include

from ovp.apps.core import views


urlpatterns = [
    url("^startup/$", views.startup, name="startup"),
    url("^contact/$", views.contact, name="contact"),
    url("^lead/$", views.record_lead, name="lead"),
    url("^footprint/$", views.footprint, name="footprint"),
    url("^ready/$", views.ready, name="ready"),
    url("^clear-ratings/$", views.clear_ratings, name="clear_ratings"),
    url("^pix/$", views.pixel, name="pixel"),
]

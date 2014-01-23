"""URLs for the command_interface app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.CommandInterfaceMainView.as_view(),
        name='command_interface_main'),
)

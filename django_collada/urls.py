# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from django_collada.views import home, three_js
from django_collada.services import get_foobar_properties


urlpatterns = patterns('django_collada.views',
    url(r'^django_collada/$', home, name='django_collada_home'),
    url(r'^django_collada/three_js/$', three_js, name='django_collada_three_js'),
)

urlpatterns += [
    url(r'^django_collada/get_foobar_properties/(?P<foobar_scene_id>[a-zA-Z0-9]+)/$', get_foobar_properties, name='django_collada_get_foobar_properties'),
]

# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import *

from models import *

@login_required
def get_foobar_properties(request, foobar_scene_id):

    if request.method == 'GET':
        foobar_scene = FooBarScene.objects.get(pk=int(foobar_scene_id))
        return HttpResponse(foobar_scene.get_scene_properties_as_json(), content_type="application/json")
    else:
        raise HttpResponseNotAllowed(['GET'])
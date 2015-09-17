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
def home(request):
    template_data = dict()

    return render_to_response("django_collada_home.html", template_data, context_instance=RequestContext(request))


@login_required
def three_js(request):

    template_data = dict()
    template_data['scenes'] = FooBarScene.objects.all()

    # TODO: add persistent model for this when we know how it should look like
    template_data['3js_config'] = {
        'background_color': 'd0d0d0',
        'background_alpha': 1,
        'show_grid': True,                      # Display grid in XY-plane
        'show_axes': True,                      # Show red, green and blue axes extending from origo
        'camera_controls': True,                # Will let user take control to pan, zoom and rotate camera
        'camera_animation': False,              # Will circle around in all 3 axis, all sides will be covered
        'camera_overview_rotation': True,       # Will rotate camera in a circle looking down, useful for scenes where the ground or table is used
        'camera_overview_rotation_speed': 4,    # 2 means 30 sec per lap on 60 FPS render speed.
        'show_stats': False,
        'x_pos': -0.2,
        'y_pos': 0,
        'z_pos': 0.1,
    }

    if request.method == 'GET':
        scene_id = request.GET.get('scene_id', None)
        if scene_id is not None:
            scene = FooBarScene.objects.get(pk=int(scene_id))

            # refresh the quick_collada structure
            scene.save()

            template_data['selected_scene'] = scene

    return render_to_response(
        "django_collada_three_js/django_collada_three_js_example.html",
        template_data,
        context_instance=RequestContext(request))

# django-collada
A Django application that adds support for uploading and visualizing a Collada model.

## About
This component was developed during the project "E-moln", a project partially financed by the Swedish governmental agency Energimyndigheten.

## Installation
First switch to the virtual environment of choice.

```
$ git clone https://github.com/iGW/django-collada
cd django-collada
python ./setup.py install
```

## Usage


### Installing the example application
This is an optional step if you want to take a look at the supplied demo application.

Add django-collada to your INSTALLED_APPS in settings.py.

Synchronize the models using either south or django migrations.


### Creating Django models with 3D-awareness
A simple models.py utilizing the django-collada component could look something like this:

```
from django.db import models
from django-collada.models import ColladaScene

class Building(ColladaScene):
    name = models.CharField(max_length=64, default='My house')
```

The views.py should then look something like this:
```
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import Building

def building(request, building_id):

    template_data = dict()

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
        scene = Building.objects.get(pk=int(building_id))

        # refresh the quick_collada structure
        scene.save()

        template_data['building_scene'] = building_scene

    return render_to_response(
        "building_scene.html",
        template_data,
        context_instance=RequestContext(request))

```

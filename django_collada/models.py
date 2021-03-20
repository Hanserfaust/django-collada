import random
import hashlib
import zipfile, os, os.path
import shutil
import collada
import json

from django.dispatch import receiver
from django.db import models
from django.conf import settings


def scene_filename(instance, filename):
    # Add hash to filename
    number = random.randint(0, 1e12)
    hd = hashlib.md5(str(number)+filename).hexdigest()
    filename_hash = u'%s' % (hd[0:16])

    return "/".join(['django_collada/scenes', filename_hash, filename])


class ColladaScene(models.Model):
    file        = models.FileField(upload_to=scene_filename, blank=True)
    filesystem_path = models.TextField(default='', blank=True)
    dae_file    = models.CharField(max_length=256, blank=True, null=True)
    type_choices = (
        ('dae', 'Collada file'),
        ('zip', 'Collada ZIP archive (.dae + related assets)'),
    )
    file_type   = models.CharField(choices=type_choices, default='zip', max_length=16, blank=True)
    name        = models.CharField(max_length=32, blank=True)
    description = models.CharField(max_length=256, blank=True)
    created     = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    # During file upload, we can place useful metadata here for quick and easy access
    quick_collada = models.TextField(default='', blank=True)

    # Transient collada data
    _cached_collada_data = None

    class Meta:
        ordering = ['-created', 'name']

    def get_dae_media_path(self):
        # shop up the path and extract first part of filename as a readable name
        path = self.file.name.split('/')[:-1]
        return '%s%s/%s' % (settings.MEDIA_URL, '/'.join(path), self.dae_file)

    def get_dae_filesystem_path(self):
        # shop up the path and extract first part of filename as a readable name
        path = self.file.name.split('/')[:-1]
        return '%s/%s/%s' % (settings.MEDIA_ROOT, '/'.join(path), self.dae_file)

    def save(self, *args, **kwargs):
        # Set a default name
        # /some/path/station_building.zip becomes station_building
        if self.name is None or self.name == '':
            name_base = self.file.name.split('/')[-1].split('.')[0]
            better = name_base.replace('_', ' ').replace('.', ' ').replace('-', ' ')
            better_upper = better[:1].upper() + better[1:]
            self.name = better_upper

        super(ColladaScene, self).save(*args, **kwargs)

        # Convert file and dir into absolute paths
        fullpath = self.file.path
        dirname = os.path.dirname(fullpath)

        if fullpath.endswith(".dae"):
            self.dae_file = fullpath.split('/')[-1]
            self.file_type = 'dae'
            self.filesystem_path = self.get_dae_filesystem_path()

        elif fullpath.endswith(".zip"):

            try:
                handle = open(fullpath, 'r')
            except IOError:
                # Will happen during subsequent saves, since the .zip-file was deleted first time.
                return

            zfobj = zipfile.ZipFile(handle)
            for name in zfobj.namelist():
                if name.endswith('/'):
                    try:  # Don't try to create a directory if exists
                        os.mkdir(os.path.join(dirname, name))
                    except:
                        pass
                else:
                    outfile = open(os.path.join(dirname, name), 'wb')
                    outfile.write(zfobj.read(name))
                    outfile.close()

                    # Grab .dae file for future references
                    if name.endswith(".dae"):
                        self.dae_file = name
                        self.file_type = 'zip'
                        self.filesystem_path = self.get_dae_filesystem_path()

            # Now try and delete the uploaded .zip file and the
            # stub __MACOSX dir if they exist.
            try:
                os.remove(fullpath)
            except:
                pass

            try:
                osxjunk = os.path.join(dirname, '__MACOSX')
                shutil.rmtree(osxjunk)
            except:
                pass

        self.build_collada_cache()
        super(ColladaScene, self).save(*args, **kwargs)

    # deprecated name
    def get_quick_collada(self):
        return self.get_collada_cache()

    def get_collada_cache(self):
        return json.loads(self.quick_collada)

    def build_collada_cache(self):

        try:
            # TODO: Implement other means of getting named objects, generic way??
            named_objects = self.get_named_objects_sketchup()

        except Exception as e:
            # Return silently
            return

        collada_cache = {'named_objects': named_objects}

        collada_cache_as_json = json.dumps(collada_cache)

        self.quick_collada = collada_cache_as_json

    '''
        Map geometry-id to name for later easy reference in javascript world for example

        Note 'name' may not be a generic property of collada objects, but stem from the sketchup application

    '''
    def get_named_objects_sketchup(self):
        result = dict()
        collada_data = self.get_collada_data()

        for element in collada_data.scene.xmlnode._children[0]._children:
            try:
                name = element.attrib['name']
                id = element.attrib['id']

                if len(id) > 0 and len(name) > 0:
                    result[id] = name
            except Exception:
                pass

        return result

    def get_collada_data(self):
        if self._cached_collada_data is not None:
            collada_data = self._cached_collada_data
        else:
            collada_data = collada.Collada(self.filesystem_path)
            self._cached_collada_data = collada_data
        return collada_data

    def __unicode__(self):
        return self.name

# Auto-delete files from filesystem when they are unneeded:
@receiver(models.signals.post_delete, sender=ColladaScene)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `FileBasedScene` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


"""
    Below is an example domain extending the ColladaScene with a data source reference.

    I did not bother with making the data source stuff a generic implementation as
    they are probably very domain specific on both ends (visual side <-> data object)

    In the case below (see also service.py), the data is connected through a mapper
    object. The mapper object relates another Model object (ie database), but could
    of course instead reach out and find any data source you find suitable, by web
    service call, a sensor on a serial port or whatever...

"""
# Possibly unrelated object with no knowledge whatsoever about being visualised
class FooBar(models.Model):
    x_coord    = models.FloatField(default=0.0)
    y_coord    = models.FloatField(default=0.0)
    z_coord    = models.FloatField(default=0.0)
    color      = models.CharField(max_length=16, default='ABCDEF')

    def __unicode__(self):
        return u'x=%s, y=%s, z=%s, color=%s' % (self.x_coord, self.y_coord, self.z_coord, self.color)

# Example on how to link a specific node in a model to a data object (of type FooBar)
class SceneToDataSourceMapping(models.Model):
    node_id  = models.CharField(max_length=32)
    foobar   = models.ForeignKey(FooBar)

    def get_abs_x(self):
        return self.foobar.x_coord

    def get_abs_y(self):
        return self.foobar.y_coord

    def get_abs_z(self):
        return self.foobar.z_coord

    def get_color(self):
        return self.foobar.color

    def as_dict(self):
        # Returns all data as named dict

        return {'node_id': self.node_id,
                'x': self.get_abs_x(),
                'y': self.get_abs_y(),
                'z': self.get_abs_z(),
                'color': self.get_color()}

    def __unicode__(self):
        return u'%s to %s' % (self.node_id, self.foobar)


class FooBarScene(ColladaScene):
    data_source_mappings = models.ManyToManyField(SceneToDataSourceMapping, blank=True)
    update_interval = models.IntegerField(default=10000)

    # Returns x,y,z and color for all data_source mappings
    def get_scene_properties_as_json(self):
        result = list()

        for dsm in self.data_source_mappings.all():
            result.append(dsm.as_dict())

        return json.dumps(result)

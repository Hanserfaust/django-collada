import collada
from unittest import TestCase


class ColladaTests(TestCase):

    def test_should_find_commented_objects_in_mesh(self):
        #file = open('./test_resources/3wall.dae')
        file = open('./test_resources/blue_house.dae')
        collada_data = collada.Collada(file)

        for item in collada_data.scene.nodes:
            for child in item.children:
                self.assertEqual('ID2', child.id)


class DjangoColladaTests(TestCase):

    def test_should_create_django_collada_instance(self):
        pass

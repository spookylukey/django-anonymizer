import os
import sys

from django.conf import settings
from django.utils import unittest
from django.test import TestCase

from anonymizer import introspect
import anonymizer.tests.testapp.models

class TestIntrospect(unittest.TestCase):

    def setUp(self):
        self._old_INSTALLED_APPS = settings.INSTALLED_APPS
        settings.INSTALLED_APPS = settings.INSTALLED_APPS[:] + ["anonymizer.tests.testapp"]
        from django.db.models.loading import cache
        cache._populate()

    def tearDown(self):
        settings.INSTALLED_APPS = self._old_INSTALLED_APPS

    def test_eveything(self):
        mod = introspect.create_anonymizers_module(anonymizer.tests.testapp.models)
        expected = """
from anonymizer.tests.testapp.models import Other, EverythingModel
from anonymizer import Anonymizer

class OtherAnonymizer(Anonymizer):

    model = Other

    attributes = [
         # Skipping field id
    ]


class EverythingModelAnonymizer(Anonymizer):

    model = EverythingModel

    attributes = [
         # Skipping field id
        ('username', "username"),
        ('name', "name"),
        ('email', "email"),
        ('address_city', "city"),
        ('address_post_code', "uk_postcode"),
        ('address', "full_address"),
         # Skipping field o1_id
        ('something', "lorem"),
        ('birthday', "datetime"),
        ('age', "positive_small_integer"),
        ('icon', UNKNOWN_FIELD),
    ]
"""
        self.assertEqual(mod.strip(), expected.strip())


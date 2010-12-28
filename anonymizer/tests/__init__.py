from datetime import datetime, timedelta, date
import os
import sys

from django.conf import settings
from django.utils import unittest
from django.test import TestCase

from anonymizer import Anonymizer, introspect
from anonymizer.tests import testapp


class TestIntrospect(TestCase):

    def test_eveything(self):
        mod = introspect.create_anonymizers_module(testapp.models)
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
        ('something_else', "lorem"),
        ('some_varchar', "varchar"),
        ('birthday', "datetime"),
        ('age', "positive_small_integer"),
        ('icon', UNKNOWN_FIELD),
        ('some_datetime', "datetime"),
        ('some_date', "date"),
    ]
"""
        self.assertEqual(mod.strip(), expected.strip())

class TestAnonymizer(TestCase):

    # Nice high count, so that our handling of unique constraint with test data
    # will likely be tested.
    NUM_ITEMS = 1000

    def setUp(self):
        self.o1 = testapp.models.Other.objects.create()
        for x in xrange(0, self.NUM_ITEMS):
            d = datetime.now() + timedelta(365*x)
            testapp.models.EverythingModel.objects.create(o1=self.o1,
                                                          username="intial%d" % x,
                                                          birthday=d,
                                                          age=x,
                                                          some_datetime=datetime.now(),
                                                          some_date=date.today(),
                                                          )

    def test_eveything(self):
        # Test for as much as possible in one test.
        assert testapp.models.EverythingModel.objects.count() == self.NUM_ITEMS
        assert testapp.models.EverythingModel._meta.get_field_by_name('username')[0].unique == True

        class EverythingAnonmyizer(Anonymizer):
            model = testapp.models.EverythingModel

            attributes = [
                ('username', 'username'),
                ('name', "name"),
                ('email', "email"),
                ('address_city', "city"),
                ('address_post_code', "uk_postcode"),
                ('address', "full_address"),
                ('something', "lorem"),
                ('something_else', "similar_lorem"),
                ('some_varchar', "varchar"),
                ('birthday', "datetime"),
                ('age', "positive_small_integer"),
                ('some_datetime', "datetime"),
                ('some_date', "date"),
            ]

        EverythingAnonmyizer().run()
        objs = testapp.models.EverythingModel.objects.all()
        self.assertEqual(len(objs), self.NUM_ITEMS)
        for o in objs:
            # check everything has been changed
            self.assertFalse(o.username.startswith('initial'))
            # Check for corresponding user names/emails.  This works if username
            # is first in the list, as recommended and as introspection
            # generates.
            self.assertTrue(o.email.startswith(o.username))


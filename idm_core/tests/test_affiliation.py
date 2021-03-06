import datetime
from unittest import mock

from django.test import TestCase
from django.utils import timezone

from idm_core.person.models import Person
from idm_core.organization.models import Organization, AffiliationType, Affiliation


class CreationTestCase(TestCase):
    fixtures = ['initial']

    def setUp(self):
        self.organization = Organization.objects.create(label='Department of Metaphysics')
        self.affiliation_type = AffiliationType.objects.get(pk='staff:employee')

    def testForthcomingAffiliation(self):
        person = Person.objects.create()
        affiliation = Affiliation(identity=person,
                                  organization=self.organization,
                                  start_date=timezone.now() + datetime.timedelta(1),
                                  type=self.affiliation_type)
        affiliation.save()
        self.assertEqual(affiliation.state, 'forthcoming')

    def testActiveAffiliation(self):
        person = Person.objects.create()
        affiliation = Affiliation(identity=person,
                                  organization=self.organization,
                                  start_date=timezone.now() - datetime.timedelta(1),
                                  type=self.affiliation_type)
        affiliation.save()
        self.assertEqual(affiliation.state, 'active')

    def testHistoricAffiliation(self):
        person = Person.objects.create()
        affiliation = Affiliation(identity=person,
                                  organization=self.organization,
                                  start_date=timezone.now() - datetime.timedelta(2),
                                  end_date=timezone.now() - datetime.timedelta(1),
                                  type=self.affiliation_type)
        affiliation.save()
        self.assertEqual(affiliation.state, 'historic')

    def testSuspendForthcomingAffiliation(self):
        # Suspending a non-active affiliation shouldn't result in a state of suspended
        person = Person.objects.create()
        affiliation = Affiliation(identity=person,
                                  organization=self.organization,
                                  start_date=timezone.now() + datetime.timedelta(1),
                                  type=self.affiliation_type)
        affiliation.save()
        self.assertEqual(affiliation.state, 'forthcoming')
        self.assertEqual(affiliation.suspended, False)
        affiliation.suspend()
        self.assertEqual(affiliation.state, 'forthcoming')
        self.assertEqual(affiliation.suspended, True)

    def testSuspendActiveAffiliation(self):
        person = Person.objects.create()
        affiliation = Affiliation(identity=person,
                                  organization=self.organization,
                                  type=self.affiliation_type)
        affiliation.save()
        self.assertEqual(affiliation.state, 'active')
        self.assertEqual(affiliation.suspended, False)
        affiliation.suspend()
        self.assertEqual(affiliation.state, 'suspended')
        self.assertEqual(affiliation.suspended, True)
        affiliation.unsuspend()
        self.assertEqual(affiliation.state, 'active')
        self.assertEqual(affiliation.suspended, False)

    @mock.patch('django.utils.timezone.now')
    def testSuspendUntil(self, now):
        now.return_value = datetime.datetime(1970, 1, 1).replace(tzinfo=timezone.utc)
        person = Person.objects.create()
        affiliation = Affiliation(identity=person,
                                  organization=self.organization,
                                  type=self.affiliation_type)
        affiliation.save()
        now.return_value = datetime.datetime(1970, 1, 2).replace(tzinfo=timezone.utc)
        affiliation.suspend(until=datetime.datetime(1970, 1, 3).replace(tzinfo=timezone.utc))
        self.assertEqual(affiliation.state, 'suspended')
        now.return_value = datetime.datetime(1970, 1, 4).replace(tzinfo=timezone.utc)
        affiliation._time_has_passed()
        self.assertEqual(affiliation.state, 'active')

    @mock.patch('django.utils.timezone.now')
    def testTimePassing(self, now):
        now.return_value = datetime.datetime(1970, 1, 1).replace(tzinfo=timezone.utc)
        person = Person.objects.create()
        affiliation = Affiliation(identity=person,
                                  organization=self.organization,
                                  start_date=datetime.datetime(1970, 1, 2).replace(tzinfo=timezone.utc),
                                  end_date=datetime.datetime(1970, 1, 4).replace(tzinfo=timezone.utc),
                                  type=self.affiliation_type)
        affiliation.save()
        self.assertEqual(affiliation.state, 'forthcoming')
        now.return_value = datetime.datetime(1970, 1, 3).replace(tzinfo=timezone.utc)
        affiliation._time_has_passed()
        self.assertEqual(affiliation.state, 'active')
        now.return_value = datetime.datetime(1970, 1, 5).replace(tzinfo=timezone.utc)
        affiliation._time_has_passed()
        self.assertEqual(affiliation.state, 'historic')

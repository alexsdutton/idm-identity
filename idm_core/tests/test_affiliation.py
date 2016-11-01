import datetime
from unittest import mock

from django.utils import timezone
from django.test import TestCase

from idm_core.models import Identity
from idm_core.org_relationship.models import AffiliationType, Affiliation
from idm_core.organization.models import Organization


class CreationTestCase(TestCase):
    fixtures = ['initial']

    def setUp(self):
        self.organization = Organization.objects.create(label='Department of Metaphysics')
        self.affiliation_type = AffiliationType.objects.get(pk='staff')

    def testForthcomingAffiliation(self):
        identity = Identity.objects.create()
        affiliation = Affiliation(identity=identity,
                                  organization=self.organization,
                                  start_date=timezone.now() + datetime.timedelta(1),
                                  type=self.affiliation_type)
        affiliation.save()
        self.assertEqual(affiliation.state, 'forthcoming')

    def testActiveAffiliation(self):
        identity = Identity.objects.create()
        affiliation = Affiliation(identity=identity,
                                  organization=self.organization,
                                  start_date=timezone.now() - datetime.timedelta(1),
                                  type=self.affiliation_type)
        affiliation.save()
        self.assertEqual(affiliation.state, 'active')

    def testHistoricAffiliation(self):
        identity = Identity.objects.create()
        affiliation = Affiliation(identity=identity,
                                  organization=self.organization,
                                  start_date=timezone.now() - datetime.timedelta(2),
                                  end_date=timezone.now() - datetime.timedelta(1),
                                  type=self.affiliation_type)
        affiliation.save()
        self.assertEqual(affiliation.state, 'historic')

    def testSuspendForthcomingAffiliation(self):
        # Suspending a non-active affiliation shouldn't result in a state of suspended
        identity = Identity.objects.create()
        affiliation = Affiliation(identity=identity,
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
        identity = Identity.objects.create()
        affiliation = Affiliation(identity=identity,
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
        identity = Identity.objects.create()
        affiliation = Affiliation(identity=identity,
                                  organization=self.organization,
                                  type=self.affiliation_type)
        affiliation.save()
        affiliation.suspend(until=datetime.datetime(1970, 1, 2).replace(tzinfo=timezone.utc))
        self.assertEqual(affiliation.state, 'suspended')
        now.return_value = datetime.datetime(1970, 1, 3).replace(tzinfo=timezone.utc)
        affiliation._time_has_passed()
        self.assertEqual(affiliation.state, 'active')

    @mock.patch('django.utils.timezone.now')
    def testTimePassing(self, now):
        now.return_value = datetime.datetime(1970, 1, 1).replace(tzinfo=timezone.utc)
        identity = Identity.objects.create()
        affiliation = Affiliation(identity=identity,
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
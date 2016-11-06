import kombu
import mock
from django.db import transaction
from django.test import TransactionTestCase
from kombu.message import Message

from idm_core import broker
from idm_core.person.models import Person


class NotificationTestCase(TransactionTestCase):
    def testPersonCreate(self):
        with broker.connection.acquire(block=True) as conn:
            queue = kombu.Queue(exclusive=True).bind(conn)
            queue.declare()
            queue.bind_to(exchange=kombu.Exchange('idm.core.person'), routing_key='#')
            with transaction.atomic():
                person = Person()
                person.save()
            message = queue.get()
            assert message is not None
            assert isinstance(message, Message)
            self.assertEqual(message.delivery_info['routing_key'],
                             'created.{}'.format(str(person.id)))
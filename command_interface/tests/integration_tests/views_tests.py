"""Tests for the views of the ``command_interface`` app."""
import os
import subprocess

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.test.client import RequestFactory

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin
from mock import patch

from ...views import CommandInterfaceMainView


class CommandInterfaceViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``CommandInterfaceView`` view class."""
    longMessage = True

    def assertRedirects(self, response, location=None, msg=None):
        """Overridden assertRedirects to use RequestFactories."""
        if msg is None:
            msg = 'Response did not redirect as expected'
        # if location is None, we assume redirect to login
        if location is None:
            location = '{0}?next={1}'.format(
                settings.LOGIN_URL, self.get_url())

        self.assertEqual(
            response.status_code, 302, msg=msg)
        self.assertEqual(
            response['Location'], location, msg=msg)

    def get_view_name(self):
        return 'command_interface_main'

    def setUp(self):
        self.regular_user = UserFactory()
        self.admin = UserFactory(is_superuser=True)
        self.req = RequestFactory().get(self.get_url())
        self.view = CommandInterfaceMainView.as_view()

        command = 'mycommand'
        self.data = {'command': command}
        self.post_req = RequestFactory().post(self.get_url(), data=self.data)
        manage_py = os.path.join(settings.DJANGO_PROJECT_ROOT, 'manage.py')
        self.called_with = ['/.{0}'.format(manage_py), command]

    @patch.object(subprocess, 'Popen')
    def test_view(self, popen_mock):
        # Anonymous users should be redirected to login
        self.req.user = AnonymousUser()
        resp = self.view(self.req)
        self.assertRedirects(resp)

        # Also regular users should be redirected to login
        self.req.user = self.regular_user
        resp = self.view(self.req)
        self.assertRedirects(resp)

        # Admins should be able to call the view
        self.req.user = self.admin
        resp = self.view(self.req)
        self.assertEqual(resp.status_code, 200, msg=(
            'Superusers should be able to call the view.'))

        self.post_req.user = self.admin
        resp = self.view(self.post_req)
        self.assertRedirects(resp, self.get_url())
        # test if the command was called.
        popen_mock.assert_called_with(self.called_with)

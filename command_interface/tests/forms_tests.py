"""Tests for the forms of the ``command_interface`` app."""
import os
import subprocess

from django.conf import settings
from django.test import TestCase

from mock import patch

from ..forms import CommandExecutionForm


class CommandExecutionFormTestCase(TestCase):
    """Tests for the ``CommandExecutionForm`` form class."""
    longMessage = True

    def setUp(self):
        command = 'mycommand'
        self.data = {'command': command}
        manage_py = os.path.join(settings.DJANGO_PROJECT_ROOT, 'manage.py')
        self.called_with = ['/.{0}'.format(manage_py), command]

    @patch.object(subprocess, 'Popen')
    def test_form(self, popen_mock):
        form = CommandExecutionForm(self.data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        form.execute()
        popen_mock.assert_called_with(self.called_with)

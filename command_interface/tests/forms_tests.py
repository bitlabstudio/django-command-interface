"""Tests for the forms of the ``command_interface`` app."""
import subprocess

from django.test import TestCase

from mock import patch

from ..forms import CommandExecutionForm


class CommandExecutionFormTestCase(TestCase):
    """Tests for the ``CommandExecutionForm`` form class."""
    longMessage = True

    def setUp(self):
        self.data = {'command': 'mycommand'}

    @patch.object(subprocess, 'Popen')
    def test_form(self, popen_mock):
        form = CommandExecutionForm(self.data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        form.execute()
        popen_mock.assert_called()

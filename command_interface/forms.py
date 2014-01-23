"""Forms for the ``command_interface`` app."""
import os
import subprocess

from django import forms
from django.conf import settings


class CommandExecutionForm(forms.Form):
    """Form, that executes a manage.py command."""

    command = forms.CharField()

    def execute(self):
        """
        Calls the command, that was entered.

        :test_run: Only required by testrunners, so that we wait for the
          command to finish.
        """
        command = self.cleaned_data.get('command')
        manage_py = os.path.join(settings.DJANGO_PROJECT_ROOT, 'manage.py')
        subprocess.Popen(['/.{0}'.format(manage_py), command])

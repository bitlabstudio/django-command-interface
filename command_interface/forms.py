"""Forms for the ``command_interface`` app."""
import os
import subprocess
from collections import namedtuple

from django import forms
from django.conf import settings
from django.core.management import get_commands, load_command_class
from django.utils.translation import ugettext_lazy as _

from . import settings as app_settings


class CommandExecutionForm(forms.Form):
    """Form, that executes a manage.py command."""

    command = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(CommandExecutionForm, self).__init__(*args, **kwargs)
        self.command_dict = get_commands()
        self.allowed_commands = []
        apps = {}
        for command_name, app_name in self.command_dict.iteritems():
            if self.command_allowed(command_name, app_name):
                self.allowed_commands.append(command_name)
                command_class = load_command_class(app_name, command_name)
                Command = namedtuple('Command', ['command', 'docstring'])
                if command_class.__doc__ is not None:
                    docstring = command_class.__doc__
                else:
                    docstring = getattr(command_class, 'help',
                                        _('No docs available.'))
                command = Command(command_name, docstring)
                if not app_name in apps:
                    App = namedtuple(app_name.replace('.', '_'),
                                     ['app_name', 'commands'])
                    apps[app_name] = App(app_name, [command])
                else:
                    apps[app_name].commands.append(command)
        self.apps = apps.values()

    def clean(self):
        cleaned_data = super(CommandExecutionForm, self).clean()
        command = cleaned_data.get('command')
        if command not in self.allowed_commands:
            raise forms.ValidationError(_(
                'The command you tried to execute is not among the permitted'
                ' ones.'))
        return cleaned_data

    def command_allowed(self, command_name, app_name):
        """Returns whether or not the command or app should be listed."""
        if not app_settings.DISPLAYED_APPS and \
                not app_settings.DISPLAYED_COMMANDS:  # pragma: nocover
            return True
        if command_name in app_settings.DISPLAYED_COMMANDS or \
                app_name in app_settings.DISPLAYED_APPS:
            return True
        return False

    def execute(self):
        """
        Calls the command, that was entered.

        :test_run: Only required by testrunners, so that we wait for the
          command to finish.
        """
        command = self.cleaned_data.get('command')
        manage_py = os.path.join(settings.DJANGO_PROJECT_ROOT, 'manage.py')
        subprocess.Popen(['/.{0}'.format(manage_py), command])

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
    arguments = forms.CharField(
        label=_('Arguments'),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(CommandExecutionForm, self).__init__(*args, **kwargs)
        self.command_dict = get_commands()
        self.allowed_commands = []
        apps = {}
        for command_name, app_name in self.command_dict.iteritems():
            if self.command_allowed(command_name, app_name):
                self.allowed_commands.append(command_name)
                command_class = load_command_class(app_name, command_name)
                # creating an optionparser
                optparser = command_class.create_parser(
                    './manage.py', command_name)
                # get the docstring from the parser
                docstring = optparser.usage.replace('%prog', './manage.py')
                # get the options
                options = []
                Option = namedtuple('Option', ['opt_string', 'help'])
                for opt in optparser.option_list:
                    if opt.dest is not None:
                        dest = opt.dest.upper()
                    else:
                        dest = ''
                    opt_string = ','.join(opt._long_opts)
                    if dest:
                        opt_string += '={0}'.format(dest)
                    if opt._short_opts:
                        opt_string = '{0} {1}, '.format(
                            ','.join(opt._short_opts), dest) + opt_string
                    options.append(Option(opt_string, opt.help))

                Command = namedtuple('Command', ['command', 'docstring',
                                                 'options'])
                if command_class.__doc__ is not None:
                    # in case there's a docstring on the class, prepend it to
                    # make sure all description is included.
                    docstring = command_class.__doc__ + '\n\n' + docstring

                command = Command(command_name, docstring, options)
                App = namedtuple(app_name.replace('.', '_'),
                                 ['app_name', 'commands'])
                if not app_name in apps:
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
        arguments = self.cleaned_data.get('arguments')
        project_root = getattr(settings, 'DJANGO_PROJECT_ROOT',
                               settings.PROJECT_ROOT)
        manage_py = os.path.join(project_root, 'manage.py')
        popen_args = ['/.{0}'.format(manage_py), command]
        if arguments:
            popen_args.append(arguments)
        subprocess.Popen(popen_args)

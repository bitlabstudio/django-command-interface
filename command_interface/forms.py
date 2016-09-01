"""Forms for the ``command_interface`` app."""
import os
import subprocess
from collections import namedtuple

from django import forms
from django.conf import settings
from django.core.management import get_commands, load_command_class
from django.utils.translation import ugettext_lazy as _

from . import settings as app_settings
from .exceptions import CommandError


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
                docstring = ''
                if optparser.usage is not None:
                    docstring = optparser.usage.replace('%prog', './manage.py')
                # get the options
                options = []
                Option = namedtuple('Option', ['opt_string', 'help'])
                for opt in getattr(optparser, 'option_list', []):
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
                                                 'options', 'log'])
                if command_class.__doc__ is not None:
                    # in case there's a docstring on the class, prepend it to
                    # make sure all description is included.
                    docstring = command_class.__doc__ + '\n\n' + docstring

                log = None
                if app_settings.LOGFILE_PATH is not None:
                    file_name = os.path.join(
                        app_settings.LOGFILE_PATH,
                        'command_interface_log-{0}.log'.format(command_name))
                    try:
                        with open(file_name, 'r') as f:
                            log = f.read()
                    except IOError:
                        pass

                command = Command(command_name, docstring, options, log)
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
        project_root = settings.DJANGO_PROJECT_ROOT
        manage_py = os.path.join(project_root, 'manage.py')
        venv = os.environ.get('VIRTUAL_ENV', None)
        python = '/usr/bin/python'
        if venv is not None:
            python = os.path.join(venv, 'bin/python')
        popen_args = [python, manage_py, command]
        if arguments:
            popen_args.append(arguments)
        if app_settings.LOGFILE_PATH is not None:
            file_name = os.path.join(
                app_settings.LOGFILE_PATH,
                'command_interface_log-{0}.log'.format(command))
            try:
                with open(file_name, 'w') as f:
                    subprocess.Popen(popen_args, stdout=f, stderr=f)
            except IOError:
                raise CommandError('Could not open file for writing log.')
        else:
            subprocess.Popen(popen_args)

"""Setting defaults for the ``command_interface`` app."""
from django.conf import settings

# list of commands to explicitly display. Adds up with DISPLAYED_APPS
DISPLAYED_COMMANDS = getattr(
    settings, 'COMMAND_INTERFACE_DISPLAYED_COMMANDS', [])

# which apps should be displayed on the main view. Same syntax is as in
# INSTALLED_APPS
DISPLAYED_APPS = getattr(settings, 'COMMAND_INTERFACE_DISPLAYED_APPS', [])

# absolute path, where the log files should be stored. All files will be
# prefixed with "command_interface_log-"
LOGFILE_PATH = getattr(settings, 'COMMAND_INTERFACE_LOGFILE_PATH', None)

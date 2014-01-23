"""Views for the command_interface app."""
from collections import namedtuple

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.management import get_commands, load_command_class
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from .forms import CommandExecutionForm


class CommandInterfaceMainView(FormView):
    """
    A view, that should allow a superuser to call management commands from
    one single view within one click (or some parameters and a click).

    """
    form_class = CommandExecutionForm
    template_name = 'command_interface/command_interface_main.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect_to_login(next=request.path)
        return super(CommandInterfaceMainView, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
        form.execute()
        return super(CommandInterfaceMainView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(CommandInterfaceMainView, self).get_context_data(**kwargs)
        command_dict = get_commands()
        apps = {}
        for command_name, app_name in command_dict.iteritems():
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

        ctx.update({'apps': apps.values()})
        return ctx

    def get_success_url(self):
        return reverse('command_interface_main')

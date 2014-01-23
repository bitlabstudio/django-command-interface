"""Views for the command_interface app."""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.utils.decorators import method_decorator

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

    def get_success_url(self):
        return reverse('command_interface_main')

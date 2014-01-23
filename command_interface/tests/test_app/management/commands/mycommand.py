"""Just a dummy test command, that can be used in other tests."""
import sys

from django.core.management import BaseCommand

from django_libs.tests.factories import UserFactory


class Command(BaseCommand):
    """Creates a user, that can be detected in tests."""

    def handle(self, *args, **options):
        # NOTE WARNING!
        # When you use this in a test run, due to it being spawned in a
        # subprocess, it will write into the real database, not the test-only
        # database! Still need to figure out how to get around this.
        # Keeping this though for manual testing.
        UserFactory()
        # many commands write to stderr, maybe we can fetch that later
        sys.stderr.write('Command output to stderr.\n')
        # maybe some also use stdout
        sys.stderr.write('Command output to stdout.\n')

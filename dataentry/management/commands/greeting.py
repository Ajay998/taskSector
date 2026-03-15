from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Prints a greeting message'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='The name to greet')

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        self.stdout.write(f'Hello, {name}! This is a greeting from the management command.')
        self.stderr.write('This is an error message for demonstration purposes.')
        self.stdout.write(self.style.SUCCESS('This is a success message.'))
        self.stdout.write(self.style.WARNING('This is a warning message.'))
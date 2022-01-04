import os
import subprocess

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create Django app with React templates'

    def handle(self, name=None, *args, **kwargs):
        subprocess.run('''ls''', shell=True, check=True, executable='/bin/bash')
        top_dir = os.path.join(os.getcwd(), name)
        os.makedirs(top_dir, exist_ok=True)
        self.stdout.write("It's now %s")

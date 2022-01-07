import subprocess
import site
from django.core.management.templates import TemplateCommand


class Command(TemplateCommand):
    help = 'Create Django app with React templates'

    def handle(self, **options):
        app_name = options.pop('name')
        packages = site.getsitepackages()
        if len(packages) > 0:
            source = f'{packages[0]}/reactify'
            subprocess.run(f'''
                        ls {source}
                           mkdir {app_name}/react
                           cp -a {source}/react/. {app_name}/react/
                           mkdir templates/{app_name}/
                           mkdir static
                           cp -a {source}/templates/reactify/. {app_name}/templates/{app_name}/
                           cp -a {source}/static/. {app_name}/static/
                           cp -a {source}/*.json {app_name}/
                           cp -a {source}/*.js {app_name}/
                           cd {app_name}
                           npm install
                        ''',
                           shell=True,
                           check=True,
                           executable='/bin/bash'
                           )

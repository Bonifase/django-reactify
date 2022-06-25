import subprocess
import os
import sys
import site
from django.core.management.templates import TemplateCommand


class Command(TemplateCommand):
    help = 'Create Django app with React templates'

    def handle(self, **options):
        app_name = options.pop('name')
        packages = site.getsitepackages()
        source = None

        if len(packages) > 0:
            if sys.platform.startswith('win'):
                source = f'{packages[0]}\reactify'
            elif sys.platform.startswith('linu'):
                source = f'{packages[0]}/reactify'
            else:
                source = f'{packages[0]}/reactify'
            subprocess.run(f'''
                        ls {source}
                           mkdir {app_name}/react
                           mkdir -p {app_name}/templates/{app_name}/
                           mkdir -p {app_name}/static/{app_name}/css/
                           mkdir -p {app_name}/static/{app_name}/images/

                           cp -a {source}/react/. {app_name}/react/
                           cp -a {source}/templates/*.html {app_name}/templates/
                           cp -a {source}/templates/reactify/*.html {app_name}/templates/{app_name}/
                           cp -a {source}/static/. {app_name}/static/
                           cp -a {source}/static/js/. {app_name}/static/js/
                           cp -a {source}/static/css/*.css {app_name}/static/{app_name}/css/
                           cp -a {source}/static/images/. {app_name}/static/{app_name}/images/
                           cp -a {source}/*.json {app_name}/
                           cp -a {source}/*.js {app_name}/
                           cd {app_name}
                           npm install
                        ''',
                           shell=True,
                           check=True,
                           executable='/bin/bash'
                           )

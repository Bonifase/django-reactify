import subprocess
import os
import sys
import site
from django.core.management.templates import TemplateCommand


def windows_dir(source, app_name):
    files_dir = f'''
        mkdir {app_name}\react
        mkdir -p {app_name}\templates\{app_name}\\
        mkdir -p {app_name}\static\{app_name}\css\\
        mkdir -p {app_name}\static\{app_name}\images\\
        cp -a {source}\react\. {app_name}\react\\
        cp -a {source}\templates\*.html {app_name}\templates\\
        cp -a {source}\templates\reactify\*.html {app_name}\templates\{app_name}\\
        cp -a {source}\static\. {app_name}\static\\
        cp -a {source}\static\js\. {app_name}\static\js\\
        cp -a {source}\static\css\*.css {app_name}\static\{app_name}\css\\
        cp -a {source}\static\images\. {app_name}\static\{app_name}\images\\
        cp -a {source}\*.json {app_name}\\
        cp -a {source}\*.js {app_name}\\
    '''
    return files_dir


def mac_dir(source, app_name):
    files_dir = f'''
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
    '''
    return files_dir

class Command(TemplateCommand):
    help = 'Create Django app with React templates'

    def handle(self, **options):
        app_name = options.pop('name')
        packages = site.getsitepackages()

        if len(packages) > 0:
            if sys.platform.startswith('win'):
                source = f'{packages[0]}\reactify'
                self.generate_react_packages(source, app_name, 'WIN')
            elif sys.platform.startswith('linu'):
                source = f'{packages[0]}/reactify'
                self.generate_react_packages(source, app_name, 'LIN')
            else:
                source = f'{packages[0]}/reactify'
                self.generate_react_packages(source, app_name, 'MAC')


    def generate_react_packages(self, source, app_name, platform):

        try:
            subprocess.run(
                self.react_package_directory(source, app_name, platform),
                shell=True,
                check=True,
                executable='/bin/bash'
            )
        except subprocess.CalledProcessError:
            pass


    def react_package_directory(self, source, app_name, platform):
        platform_dirs = {
            'MAC': mac_dir(source, app_name),
            'LIN': mac_dir(source, app_name),
            'WIN': windows_dir(source, app_name)
        }

        return platform_dirs[platform] + self.install_packages(app_name)


    def install_packages(self, app_name):
        command_string = f'''
            cd {app_name}
            echo "Installing react packages..."
            npm install
            echo " "
            echo "cd {app_name} and run:"
            echo "     npm run dev"
            echo " "
            echo "Happy coding 😄!"
            echo " "
        '''

        return command_string

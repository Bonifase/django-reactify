import subprocess
import os
import sys
import site
from django.core.management.templates import TemplateCommand


def windows_dir(source, app_name):
    """
    Generates a script to create directories and copy files for a specified application in a Windows environment.

    Args:
        source (str): The source directory containing the files and folders to be copied.
        app_name (str): The name of the target application for which directories and files are being set up.

    Returns:
        str: A multi-line string containing the commands to create directories and copy files.

    The generated script performs the following tasks:
    1. Creates a `react` directory under the specified `app_name`.
    2. Creates nested directories under `templates` and `static` for organizing HTML, CSS, JavaScript, and image files.
    3. Copies files from the `source` directory to the respective locations under the `app_name` directory.

    Directory and File Operations:
    - Creates the following structure under `app_name`:
        - `react/`
        - `templates/app_name/`
        - `static/app_name/css/`
        - `static/app_name/images/`
    - Copies:
        - All React files from `source/react/` to `app_name/react/`.
        - HTML files from `source/templates/` to `app_name/templates/`.
        - React-specific HTML templates from `source/templates/reactify/` to `app_name/templates/app_name/`.
        - Static files, JavaScript files, CSS files, and images to respective subdirectories under `app_name/static/`.
        - JSON and JavaScript files from the `source` root to the `app_name` root.

    Example:
        >>> script = windows_dir("C:/my_project", "my_app")
        >>> print(script)
        mkdir my_app\react
        mkdir -p my_app\templates\my_app\
        mkdir -p my_app\static\my_app\css\
        mkdir -p my_app\static\my_app\images\
        cp -a C:/my_project\react\. my_app\react\
        cp -a C:/my_project\templates\*.html my_app\templates\
        ...

    Note:
        Ensure that the `source` directory exists and contains the expected file structure for this script to execute correctly.
    """
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
    """
    Generates a script to create directories and copy files for a specified application in a macOS/Linux environment.

    Args:
        source (str): The source directory containing the files and folders to be copied.
        app_name (str): The name of the target application for which directories and files are being set up.

    Returns:
        str: A multi-line string containing the commands to create directories and copy files.

    The generated script performs the following tasks:
    1. Creates a `react` directory under the specified `app_name`.
    2. Creates nested directories under `templates` and `static` for organizing HTML, CSS, JavaScript, and image files.
    3. Copies files from the `source` directory to the respective locations under the `app_name` directory.

    Directory and File Operations:
    - Creates the following structure under `app_name`:
        - `react/`
        - `templates/app_name/`
        - `static/app_name/css/`
        - `static/app_name/images/`
    - Copies:
        - All React files from `source/react/` to `app_name/react/`.
        - HTML files from `source/templates/` to `app_name/templates/`.
        - React-specific HTML templates from `source/templates/reactify/` to `app_name/templates/app_name/`.
        - Static files, JavaScript files, CSS files, and images to respective subdirectories under `app_name/static/`.
        - JSON and JavaScript files from the `source` root to the `app_name` root.

    Example:
        >>> script = mac_dir("/Users/my_project", "my_app")
        >>> print(script)
        mkdir my_app/react
        mkdir -p my_app/templates/my_app/
        mkdir -p my_app/static/my_app/css/
        mkdir -p my_app/static/my_app/images/
        cp -a /Users/my_project/react/. my_app/react/
        cp -a /Users/my_project/templates/*.html my_app/templates/
        ...

    Note:
        Ensure that the `source` directory exists and contains the expected file structure for this script to execute correctly.
    """
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
    """
    A Django management command to create a Django app with React templates.

    Attributes:
        help (str): A brief description of the command's functionality.

    Methods:
        handle(**options):
            Processes the command-line options and initiates the setup of the Django app with React templates.
        generate_react_packages(source, app_name, platform):
            Executes the commands to create the React directory structure and install necessary packages.
        react_package_directory(source, app_name, platform):
            Returns the platform-specific directory creation and package installation script.
        install_packages(app_name):
            Generates a script for installing Node.js packages and providing instructions for the developer.
    """
    help = 'Create Django app with React templates'

    def handle(self, **options):
        """
        Handles the command execution by determining the platform and initiating React package setup.

        Args:
            **options: Command-line options passed to the management command.

        Workflow:
        - Retrieves the `name` option to use as the app name.
        - Determines the platform (Windows, Linux, or macOS).
        - Sets the source directory path for React templates based on the platform.
        - Calls `generate_react_packages` to complete the setup.
        """
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
        """
        Runs the directory setup and package installation commands for React templates.

        Args:
            source (str): The source directory containing React templates.
            app_name (str): The name of the Django app being created.
            platform (str): The platform identifier ('WIN', 'MAC', or 'LIN').

        Raises:
            subprocess.CalledProcessError: If the subprocess command fails.
        """
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
        """
        Returns the directory creation script based on the platform.

        Args:
            source (str): The source directory containing React templates.
            app_name (str): The name of the Django app being created.
            platform (str): The platform identifier ('WIN', 'MAC', or 'LIN').

        Returns:
            str: A script to set up directories and install React packages.
        """
        platform_dirs = {
            'MAC': mac_dir(source, app_name),
            'LIN': mac_dir(source, app_name),
            'WIN': windows_dir(source, app_name)
        }

        return platform_dirs[platform] + self.install_packages(app_name)

    def install_packages(self, app_name):
        """
        Generates a script to install Node.js packages and provides developer instructions.

        Args:
            app_name (str): The name of the Django app.

        Returns:
            str: A script to install React packages using npm and provide further instructions.
        """
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

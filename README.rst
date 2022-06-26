===============
Django Reactify
===============

Django Reactify is an app that allows developers to add and use React components in your Django app without using `create-react-app <https://github.com/facebookincubator/create-react-app>`_.

Quick start
-----------

1. Install the package via the following command:

    pip install django-reactify

2. Add "reactify" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'reactify',
    ]

3. Run the following command:

   Ensure that the templates directory exists in the specified app name.

    python manage.py reactify <app_name>


    - Replace the app name with the existing Django app you want to reactify.

    - This command does the following:

        * Creates barbel and webpack configuration files in the app's root directory.

        * Creates package.json file with the scripts to run React development server.

        * Creates a react folder directory with the necessary files and subdirectories where you can add your react component files and redux actions and reducers.

        * Creates a react folder directory with the necessary files and subdirectories where you can add your react component files and redux actions and reducers.

        * Installs the basic npm development packages.

        * starts the react development server that listens on the changes made to the react components and compile a minimal js file that is rendered to the view.

4. cd to the django app directory and run the following command:

    npm run dev


5. Add the new view function to the views file to render the compiled version of the react app.

    def index(request):
        template_name = '<app_name>/index.html'

        return render(request, template_name)

6. Add more React components to the react app's component folder.

Managing React Routes
---------------------
If you don't configure Django urls to accept the Routes declared in the react, you will encouter 404 error.

To fix this, lets say you have react routes as follows:

    <Switch>
        <Route exact path="/" component={Main} />

        <Route exact path="/login" component={LoginPage} />

        <Route exact path="/services" component={ServicesPage} />

        <Route exact path="/about" component={AboutPage} />

In the app urls file use `re_path`,

    from django.urls import re_path
    
    from .views import index

    urlpatterns = [
        re_path(r'', index, name="home"),
        ]

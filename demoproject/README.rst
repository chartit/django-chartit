###################
Django chartit demo
###################

This is a quick demo project to demonstrate how to draw charts.

============================
Installation & Configuration
============================

This demoproject is installed as part of the `django_chartit` package.
To install additional dependecies execute the command ::

    pip install docutils Django django-markup-deprecated pytz Pygments

To run the demo project ::

    cd demoproject/
    python ./manage.py migrate
    python ./manage.py runserver

To run the demo project from inside a git checkout ::

    cd demoproject/
    PYTHONPATH=../ python ./manage.py migrate
    PYTHONPATH=../ python ./manage.py runserver

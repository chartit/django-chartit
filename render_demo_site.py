#!/bin/env python

import os
import sys

try:
    sys.path.append('demoproject')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demoproject.settings")

    from django.conf import settings
    from django.test import Client


    settings.DATABASES['default']['NAME'] = '/tmp/chartit.demo.sqlite'

    try:
        import django
        setup = django.setup
    except AttributeError:
        raise
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements.txt")

if __name__ == "__main__":
    from demoproject.urls import urlpatterns
    from django.core.management import call_command
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile

    client = Client()
    default_storage.location = '/tmp/chartit-demo/'
    settings.STATIC_ROOT = default_storage.location + '/static/'

    # prepare DB
    result = call_command('migrate', verbosity=2)
    # collect static files
    result = call_command('collectstatic', '--noinput', verbosity=2)

    # render all views
    for url in urlpatterns:
        address = url._regex
        if address.startswith('^'):
            address = '/' + address[1:]
        if address.endswith('$'):
            address = address[:-1]
        filename = "%sindex.html" % address[1:]
        response = client.get(address)
        assert response.status_code == 200

        default_storage.save(filename, ContentFile(response.content))

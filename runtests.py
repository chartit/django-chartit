import os
import sys

try:
    sys.path.append('demoproject')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demoproject.settings")

    from django.conf import settings
    from django.core.management import call_command

    settings.DATABASES['default']['NAME'] = ':memory:'

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ["demoproject"]

    # ./manage.py test takes care of database creation and
    # application of migrations if any
    result = call_command('test', *test_args, verbosity=2, failfast=True)
    sys.exit(result)


if __name__ == "__main__":
    run_tests(*sys.argv[1:])

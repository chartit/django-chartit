# pylint: disable=missing-docstring,locally-disabled

import codecs
import re
from os import path
from setuptools import setup, find_packages


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as _fp:
        return _fp.read()


def get_version(*file_paths):
    """Get the django-chartit2 version without importing the module."""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='django_chartit',
    version=get_version('chartit', '__init__.py'),
    packages=find_packages(exclude=["demoproject.*", "demoproject",
                                    "docs.*", "docs"]),
    description=("A Django app to plot charts and pivot charts directly from "
                 "the models. Uses HighCharts and jQuery JavaScript libraries "
                 "to render the charts on the webpage."),
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
    ],
    platforms='any',
    keywords='django charts',
    author='Praveen Gollakota',
    author_email='pgollakota@gmail.com',
    maintainer='Alexander Todorov',
    maintainer_email='atodorov@mrsenko.com',
    url='https://github.com/chartit/django-chartit',
    license='BSD',
    include_package_data=True,
    zip_safe=False,
)

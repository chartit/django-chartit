from setuptools import setup, find_packages

version = 0.1

setup(
    name='django_chartit',
    version=version,
    packages=find_packages(exclude=["chartit_tests.*", "demoproject.*",
                                    "chartit_tests", "demoproject",
                                    "docs.*", "docs"]),
    requires=["simplejson"],
    description=("A Django app to plot charts and pivot charts directly from "
                 "the models. Uses HighCharts and jQuery JavaScript libraries "
                 "to render the charts on the webpage."),
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
    ],
    platforms='any',
    keywords='django charts',
    author='Praveen Gollakota',
    author_email='pgollakota@gmail.com',
    url='https://github.com/grantmcconnaughey/django-chartit2',
    license='BSD',

    include_package_data=True,
    zip_safe=False,
)

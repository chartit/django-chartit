from setuptools import setup, find_packages

import chartit

setup(
    name='django_chartit2',
    version=chartit.__version__,
    packages=find_packages(exclude=["chartit_tests.*", "demoproject.*",
                                    "chartit_tests", "demoproject",
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
    install_requires=["simplejson"],
    keywords='django charts',
    author='Praveen Gollakota',
    author_email='pgollakota@gmail.com',
    maintainer='Grant McConnaughey',
    maintainer_email='grantmcconnaughey@gmail.com',
    url='https://github.com/grantmcconnaughey/django-chartit2',
    license='BSD',
    include_package_data=True,
    zip_safe=False,
)

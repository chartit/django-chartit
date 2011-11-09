from setuptools import setup, find_packages

project = 'django_chartit'
version = 0.1
requires = ["django(>=1.3)", "simplejson"]

setup(
    name=project,
    version=version,
    packages=find_packages(exclude=["chartit_tests.*", "demoproject.*",
                                    "chartit_tests", "demoproject",
                                    "docs.*", "docs"]),
    
    # this is a django app. So requires django
    requires=requires,
    
    # metadata for upload to PyPI
    description="",
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
         'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
      ],
    platforms='any',
    keywords='django charts',
    author='Praveen Gollakota',
    author_email='pgollakota@gmail.com',
    url='http://github.com/pgollakota/django-chartit',
    license='BSD',
    
    include_package_data=True,
    zip_safe=False,
)

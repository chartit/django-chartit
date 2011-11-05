from setuptools import setup, find_packages

project = 'chartit'
version = 0.1

setup(name=project,
      version=version,
      description="",
      long_description=open('README.rst').read(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development',
      ],
      platforms='any',
      keywords='django charts',
      author='Praveen Gollakota',
      author_email='pgollakota@gmail.com',
      url='http://github.com/pgollakota/django-chartit',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
     )

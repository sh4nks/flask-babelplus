"""
Flask-BabelPlus
---------------

Adds i18n/l10n support to Flask applications with the help of the
`Babel`_ library.

This is a fork of Flask-BabelEx which in turn is a fork of the official
Flask-Babel extension. It is API compatible with both forks.

It comes with following additional features:

1. It is possible to use multiple language catalogs in one Flask application;
2. Localization domains: your extension can package localization file(s) and
   use them if necessary;
3. Does not reload localizations for each request.

The main difference to Flask-BabelEx is, that you can pass the
localization ``Domain`` in the extensions initialization process.

.. code:: python

    # Flask-BabelPlus
    babel.init_app(app=app, default_domain=FlaskBBDomain(app))


Links
`````

* `Documentation <http://packages.python.org/Flask-BabelPlus>`_
* `Flask-BabelEx <https://github.com/mrjoes/flask-babelex>`_
* `original Flask-Babel <https://pypi.python.org/pypi/Flask-Babel>`_.

.. _Babel: https://github.com/python-babel/babel

"""
from setuptools import setup


setup(
    name='Flask-BabelPlus',
    version='1.0.1',
    url='https://github.com/sh4nks/flask-babelplus',
    license='BSD',
    author='Peter Justin',
    author_email='peter.justin@outlook.com',
    description='Adds i18n/l10n support to Flask applications',
    long_description=__doc__,
    packages=['flask_babelplus'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'Babel>=1.0',
        'speaklater>=1.2',
        'Jinja2>=2.5'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

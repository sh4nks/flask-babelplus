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

The main difference to Flask-BabelEx is, that you can pass arguments to the
``init_app`` method as well.

.. code:: python

    # Flask-BabelPlus with custom domain
    babel.init_app(app=app, default_domain=FlaskBBDomain(app))


Links
`````

* `Documentation <http://packages.python.org/Flask-BabelPlus>`_
* `Flask-BabelEx <https://github.com/mrjoes/flask-babelex>`_
* `original Flask-Babel <https://pypi.python.org/pypi/Flask-Babel>`_.

.. _Babel: https://github.com/python-babel/babel

"""
import ast
import re
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTestCommand(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open('flask_babelplus/__init__.py', 'rb') as f:
    version_line = re.search(
        r'__version__\s+=\s+(.*)', f.read().decode('utf-8')
    ).group(1)
    version = str(ast.literal_eval(version_line))


setup(
    name='Flask-BabelPlus',
    version=version,
    url='https://github.com/sh4nks/flask-babelplus',
    license='BSD',
    author='Peter Justin',
    author_email='peter.justin@outlook.com',
    description='Adds i18n/l10n support to Flask applications',
    long_description=__doc__,
    packages=['flask_babelplus'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=0.9',
        'Babel>=1.0',
        'Jinja2>=2.5'
    ],
    tests_require=[
        "py",
        "pytest",
        "pytest-cov"
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
    ],
    cmdclass={"test": PyTestCommand}
)

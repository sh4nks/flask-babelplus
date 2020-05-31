Flask-BabelPlus
===============

[![Build Status](https://travis-ci.org/sh4nks/flask-babelplus.svg?branch=master)](https://travis-ci.org/sh4nks/flask-babelplus)
[![Coverage Status](https://coveralls.io/repos/github/sh4nks/flask-babelplus/badge.svg?branch=master)](https://coveralls.io/github/sh4nks/flask-babelplus?branch=master)
[![PyPI Version](https://img.shields.io/pypi/v/Flask-BabelPlus.svg)](https://pypi.python.org/pypi/Flask-BabelPlus)
[![Documentation Status](https://readthedocs.org/projects/flask-babelplus/badge/?version=latest)](https://flask-babelplus.readthedocs.io/en/latest/?badge=latest)

Adds i18n/l10n support to Flask applications with the help of the
[Babel](https://github.com/python-babel/babel) library.

This is a fork of Flask-BabelEx which in turn is a fork of the official
Flask-Babel extension. It is API compatible with both forks.

It comes with following additional features:

1. It is possible to use multiple language catalogs in one Flask application;
2. Localization domains: your extension can package localization file(s) and
   use them if necessary;
3. Does not reload localizations for each request.

The main difference to Flask-BabelEx is, that you can pass the
localization ``Domain`` in the extensions initialization process.

```python
# Flask-BabelPlus
babel.init_app(app=app, default_domain=FlaskBBDomain(app))
```


Links
=====

* [Documentation](https://flask-babelplus.readthedocs.io)
* [Flask-BabelEx](https://github.com/mrjoes/flask-babelex)
* [Original Flask-Babel Extension](https://github.com/python-babel/Flask-Babel)


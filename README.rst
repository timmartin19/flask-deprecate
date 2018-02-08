===============================
Flask-Deprecate
===============================


.. image:: https://img.shields.io/pypi/v/flask_deprecate.svg
        :target: https://pypi.python.org/pypi/flask-deprecate

.. image:: https://img.shields.io/travis/timmartin19/flask_deprecate.svg
        :target: https://travis-ci.org/timmartin19/flask-deprecate

.. image:: https://readthedocs.org/projects/flask-deprecate/badge/?version=latest
        :target: https://flask-deprecate.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Easy decorators for deprecating flask views and blueprints


* Free software: MIT license
* Documentation: https://flask-deprecate.readthedocs.io.


Example
-------

.. code-block:: python

    from flask import Flask, Response

    from flask_deprecate import deprecate_view

    app = Flask('myapp')

    @app.route('/myroute')
    @deprecate_view("Don't use this!")
    def myroute():
        return Response()

An HTTP compliant "Warning" header is injected indicating the route is
deprecated and optionally providing an upgrade path.


You can also deprecate an entire blueprint in favor of a new one

.. code-block:: python

    from flask import Flask, Response, Blueprint

    from flask_deprecate import deprecate_blueprint

    old_bp = Blueprint('old', 'old', url_prefix='/v1')
    new_bp = Blueprint('new', 'new', url_prefix='/v2')

    @old_bp.route('/my_route')
    def my_old_route():
        return Resonse()

    @new_bp.route('/my_new_route')
    def my_new_route():
        return Response()

    deprecate_blueprint(old_bp, new_blueprint=new_bp)
    app.register_blueprint(old_bp)
    app.register_blueprint(new_bp)

This will inject the Warning header for every route on the old blueprint
and additionally direct the client to use the new `/v2` api.

Documentation
-------------

You will need to install the package dependencies first,
see the Installation section for details.

To build and open the documentation simply run:

.. code-block:: bash

    bin/build-docs

Installation
------------

If you need to install pyenv/virtualenvwrapper you can run the `bin/setup-osx` command
Please note that this will modify your bash profile

Assuming you have virtualenv wrapper installed

.. code-block:: bash

    mkvirtualenv flask-deprecate
    workon flask-deprecate
    pip install -r requirements_dev.txt
    pip install -e .

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


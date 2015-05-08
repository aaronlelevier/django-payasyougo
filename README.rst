django-payasyougo
=================
A simple Django App to demonstrate the MVC structure, project structure,
and how different libraries work together.


Installation
------------
# TODO


Pythonic Highlights
-------------------
Model choices - for loop comprehension

Monkeypatch - production methods in tests when necessary


Libraries Used
--------------
`Remark <https://github.com/gnab/remark/>`_ for the Slideshow

`RST Syntax guide <http://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html#internal-and-external-links>`_


Python Packages
---------------
Django 1.8

django-rest-framework

djangular

django-nose

django-braces

model_mommy


Things that I learned while doing this
--------------------------------------
Don't have a bunch of imports for unneeded modules (clean up imports as a part of refactoring)

Sometimes it's better to use generic naming of object attributes than specific

    - ex: Main business Account Module is named ``Hotel`` instead of ``Account``

stocktrends
===========

.. image:: https://img.shields.io/pypi/v/stocktrends.svg
    :target: https://pypi.python.org/pypi/stocktrends
    :alt: Latest PyPI version

.. image:: stocktrends.png
   :target: stocktrends
   :alt: Latest Travis CI build status


Installation
------------



Usage
-----

.. code-block:: python

    from stocktrends import Renko
    renko= Renko(df)
    renko.brick_size = 2
    data = renko.get_chart_data()

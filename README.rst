stocktrends
===========

A python package to calcuate trends in stock markets.

.. image:: https://img.shields.io/pypi/v/stocktrends.svg
    :target: https://pypi.python.org/pypi/stocktrends
    :alt: Latest PyPI version

.. image:: stocktrends.png
   :target: stocktrends
   :alt: Latest Travis CI build status


Installation
------------

To install stable version from pypi, run

.. code-block:: shell

    pip install stocktrends


To install latest code from github, run

.. code-block:: shell

    pip install git+https://github.com/chillaranand/stocktrends





Usage
-----

Create OHLC dataframe.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    In [7]: import pandas as pd

    In [8]: df = pd.read_csv('/home/chillaranand/stocks/HOOLI')

    In [9]: df.head()
             date    open     high      low    close
    0  2015-01-01  143.15  146.000  141.825  143.950
    1  2015-01-02  144.05  148.025  142.150  142.775
    2  2015-01-05  142.50  145.450  137.050  137.925
    3  2015-01-06  135.00  136.500  116.000  118.050
    4  2015-01-07  118.55  129.400  118.500  127.150


Renko chart calcuation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from stocktrends import Renko


    renko = Renko(df)
    renko.brick_size = 2
    data = renko.get_ohlc_data()
    print(data.tail())


LineBreak chart calcuation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from stocktrends import LineBreak


    lb = LineBreak(df)
    lb.line_number = 3
    data = lb.get_ohlc_data()
    print(data.tail())


PnF chart calcuation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from stocktrends import PnF


    pnf = PnF(df)
    pnf.box_size = 2
    pnf.reversal_size = 3
    data = pnf.get_ohlc_data()
    print(data.tail())

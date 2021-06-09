stocktrends
===========

A python package to calcuate trends in stock markets.

.. image:: https://img.shields.io/pypi/v/stocktrends.svg
    :target: https://pypi.python.org/pypi/stocktrends
    :alt: Latest PyPI version


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

| The following code from demo.py file shows how to construct dataframe from a csv file and then plot Renko, Line Break and PnF charts.


.. code-block:: python

    """
    Sample data from tests/HDFCLIFE.csv file.

    Date,Symbol,Series,Prev Close,Open,High,Low,Last,Close,VWAP,Volume,Turnover,Trades,Deliverable Volume,%Deliverble
    2017-11-17,HDFCLIFE,EQ,290.0,310.0,369.0,307.0,343.9,344.6,327.26,168836552,5525288229115000.0,1177530,82044782,0.48590000000000005
    2017-11-20,HDFCLIFE,EQ,344.6,344.7,358.9,344.0,355.0,355.35,353.18,14650240,517410581605000.0,166263,6761287,0.4615
    2017-11-21,HDFCLIFE,EQ,355.35,356.4,418.9,352.5,386.9,385.3,389.24,43078194,1676786001315000.0,450090,11584111,0.26890000000000003
    2017-11-22,HDFCLIFE,EQ,385.3,388.0,408.0,386.9,394.0,395.2,397.38,15227642,605123098895000.0,166870,3475999,0.22829999999999998
    """

    import pandas as pd

    from stocktrends import indicators


    df = pd.read_csv('tests/HDFCLIFE.csv')
    df.columns = [i.lower() for i in df.columns]
    rows = 5

    pnf = indicators.PnF(df)
    pnf.box_size = 10
    pnf.reversal_size = 3


    print('\n\nPnF BAR data - based on "close" column')
    data = pnf.get_bar_ohlc_data(source='close')
    print(data.head(rows))


    print('\n\nPnF BOX data - based on "close" column')
    pnf_data = pnf.get_ohlc_data(source='close')
    print(pnf_data.head(rows))


    print('\n\nPnF BOX data - based on "high"/"low" columns')
    data = pnf.get_bar_ohlc_data(source='hl')
    print(data.head(rows))


    renko = indicators.Renko(df)


    print('\n\nRenko box calcuation based on periodic close')
    renko.brick_size = 2
    renko.chart_type = indicators.Renko.PERIOD_CLOSE
    data = renko.get_ohlc_data()
    print(data.tail(rows))


    # print('\n\nRenko box calcuation based on price movement')
    # renko.chart_type = indicators.Renko.PRICE_MOVEMENT
    # data = renko.get_ohlc_data()
    # print(data.tail(rows))


    lb = indicators.LineBreak(df)

    print('\n\nLine break chart')
    lb.line_number = 3
    data = lb.get_ohlc_data()
    print(data.tail(rows))

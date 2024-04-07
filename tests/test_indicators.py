import pandas as pd

from stocktrends import Renko, LineBreak

import pytest



rdf = pd.read_csv('tests/hooli_renko_4.csv')
# lbdf = pd.read_csv('tests/hooli_linebreak_3.csv')


def test_renko():
    df = pd.read_csv('HOOLI')
    renko = Renko(df)
    renko.brick_size = 4
    cdf = renko.get_ohlc_data()
    assert rdf['close'].compare(cdf['close']).empty


def test_linebreak():
    lb = LineBreak(df)
    lb.line_number = 3
    cdf = lb.get_ohlc_data()
    assert cdf['close'].compare(lbdf['close']).empty

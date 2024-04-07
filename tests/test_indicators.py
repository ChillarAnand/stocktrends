import pandas as pd

from stocktrends import Renko, LineBreak


def test_renko():
    input_file = 'HDFCLIFE_day_2018.csv'
    output_file = 'HDFCLIFE_day_2018_renko_5.csv'

    input_df = pd.read_csv(input_file)
    input_df.columns = input_df.columns.str.lower()
    output_df = pd.read_csv(output_file)

    renko = Renko(input_df)
    renko.brick_size = 5
    renko_df = renko.get_ohlc_data()
    renko_df['close'] = renko_df['close'].astype(float)

    pd.testing.assert_series_equal(renko_df['close'], output_df['close'])


def test_linebreak():
    input_file = 'HDFCLIFE_day_2018.csv'
    input_df = pd.read_csv(input_file)
    input_df.columns = input_df.columns.str.lower()

    line_break = LineBreak(input_df)
    line_break.line_number = 5
    line_break_df = line_break.get_ohlc_data()

    line_break_df['close'] = line_break_df['close'].astype(float)

    output_file = 'HDFCLIFE_day_2018_linebreak_5.csv'
    output_df = pd.read_csv(output_file)
    pd.testing.assert_series_equal(line_break_df['close'], output_df['close'])

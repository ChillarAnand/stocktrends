import pandas as pd

from stocktrends import indicators


df = pd.read_csv('tests/HDFCLIFE')
df.columns = [i.lower() for i in df.columns]


pnf = indicators.PnF(df)
pnf.box_size = 10
pnf.reversal_size = 3


print('PnF box data')
pnf_data = pnf.get_ohlc_data()
print(pnf_data.head(20))


print('PnF bar data')
bars = pnf.get_bar_ohlc_data()
print(bars.head(10))


print('PnF box data')
pnf_data = pnf.get_ohlc_data(source='hl')
print(pnf_data.head(20))


print('PnF bar data')
bars = pnf.get_bar_ohlc_data(source='hl')
print(bars.head(10))

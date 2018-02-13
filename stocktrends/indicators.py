import pandas as pd


class Instrument:

    def __init__(self, df):
        self.odf = df
        self.df = df
        self._validate_df()

    ohlc = {'open', 'high', 'low', 'close'}

    UPTREND_CONTINUAL = 0
    UPTREND_REVERSAL = 1
    DOWNTREND_CONTINUAL = 2
    DOWNTREND_REVERSAL = 3

    def _validate_df(self):
        if not self.ohlc.issubset(self.df.columns):
            raise ValueError('DataFrame should have OHLC {} columns'.format(self.ohlc))


class Renko(Instrument):

    PERIOD_CLOSE = 1
    PRICE_MOVEMENT = 2

    TREND_CHANGE_DIFF = 2

    brick_size = 1
    chart_type = PERIOD_CLOSE

    def get_ohlc_data(self):
        if self.chart_type == self.PERIOD_CLOSE:
            self.period_close_bricks()
        else:
            self.price_movement_bricks()

        return self.cdf

    def period_close_bricks(self):
        brick_size = self.brick_size
        columns = ['date', 'open', 'high', 'low', 'close']
        self.df = self.df[columns]

        self.cdf = pd.DataFrame(
            columns=columns,
            data=[],
        )

        self.cdf.loc[0] = self.df.loc[0]
        close = self.df.loc[0]['close'] // brick_size * brick_size
        self.cdf.loc[0, 1:] = [close - brick_size, close, close - brick_size, close]
        self.cdf['uptrend'] = True

        columns = ['date', 'open', 'high', 'low', 'close', 'uptrend']

        for index, row in self.df.iterrows():

            close = row['close']
            date = row['date']

            row_p1 = self.cdf.iloc[-1]
            uptrend = row_p1['uptrend']
            close_p1 = row_p1['close']

            bricks = int((close - close_p1) / brick_size)
            data = []

            if uptrend and bricks >= 1:
                for i in range(bricks):
                    r = [date, close_p1, close_p1 + brick_size, close_p1, close_p1 + brick_size, uptrend]
                    data.append(r)
                    close_p1 += brick_size
            elif uptrend and bricks <= -2:
                uptrend = not uptrend
                bricks += 1
                close_p1 -= brick_size
                for i in range(abs(bricks)):
                    r = [date, close_p1, close_p1, close_p1 - brick_size, close_p1 - brick_size, uptrend]
                    data.append(r)
                    close_p1 -= brick_size
            elif not uptrend and bricks <= -1:
                for i in range(abs(bricks)):
                    r = [date, close_p1, close_p1, close_p1 - brick_size, close_p1 - brick_size, uptrend]
                    data.append(r)
                    close_p1 -= brick_size
            elif not uptrend and bricks >= 2:
                uptrend = not uptrend
                bricks -= 1
                close_p1 += brick_size
                for i in range(abs(bricks)):
                    r = [date, close_p1, close_p1 + brick_size, close_p1, close_p1 + brick_size, uptrend]
                    data.append(r)
                    close_p1 += brick_size
            else:
                continue

            sdf = pd.DataFrame(data=data, columns=columns)
            self.cdf = pd.concat([self.cdf, sdf])

        self.cdf.reset_index(inplace=True, drop=True)
        return self.cdf

    def shift_bricks(self):
        shift = self.df['close'].iloc[-1] - self.bdf['close'].iloc[-1]
        if abs(shift) < self.brick_size:
            return
        step = shift // self.brick_size
        self.bdf[['open', 'close']] += step * self.brick_size


class LineBreak(Instrument):

    line_number = 3

    def uptrend_reversal(self, close):
        lows = [self.cdf.iloc[i]['low'] for i in range(-1, -self.line_number - 1, -1)]
        least = min(lows)
        return close < least

    def downtrend_reversal(self, close):
        highs = [self.cdf.iloc[i]['high'] for i in range(-1, -self.line_number - 1, -1)]
        highest = max(highs)
        return close > highest

    def get_ohlc_data(self):
        columns = ['date', 'open', 'high', 'low', 'close']
        self.df = self.df[columns]

        self.cdf = pd.DataFrame(columns=columns, data=[])

        for i in range(self.line_number):
            self.cdf.loc[i] = self.df.loc[i]

        self.cdf['uptrend'] = True

        columns = ['date', 'open', 'high', 'low', 'close', 'uptrend']

        for index, row in self.df.iterrows():

            close = row['close']

            row_p1 = self.cdf.iloc[-1]

            uptrend = row_p1['uptrend']

            open_p1 = row_p1['open']
            close_p1 = row_p1['close']

            if uptrend and close > close_p1:
                r = [close_p1, close, close_p1, close]
            elif uptrend and self.uptrend_reversal(close):
                uptrend = not uptrend
                r = [open_p1, open_p1, close, close]
            elif not uptrend and close < close_p1:
                r = [close_p1, close_p1, close, close]
            elif not uptrend and self.downtrend_reversal(close):
                uptrend = not uptrend
                r = [open_p1, close, open_p1, close]
            else:
                continue

            sdf = pd.DataFrame(data=[[row['date']] + r + [uptrend]], columns=columns)
            self.cdf = pd.concat([self.cdf, sdf])

        self.cdf.reset_index(inplace=True)
        return self.cdf


class PnF(Instrument):
    box_size = 1
    reversal_size = 1

    @property
    def brick_size(self):
        return self.box_size

    def get_state(self, uptrend_p1, bricks):
        state = None
        if uptrend_p1 and bricks > 0:
            state = self.UPTREND_CONTINUAL
        elif uptrend_p1 and bricks * -1 > self.reversal_size:
            state = self.UPTREND_REVERSAL
        elif not uptrend_p1 and bricks < 0:
            state = self.DOWNTREND_CONTINUAL
        elif not uptrend_p1 and bricks > self.reversal_size:
            state = self.DOWNTREND_REVERSAL
        return state

    def get_ohlc_data(self):
        brick_size = self.brick_size

        self.df = self.df[['date', 'open', 'high', 'low', 'close']]

        columns = ['date', 'open', 'high', 'low', 'close']

        self.cdf = pd.DataFrame(
            columns=columns,
            data=[],
        )

        self.cdf.loc[0] = self.df.loc[0]
        close = self.df.loc[0]['close'] // brick_size * brick_size
        self.cdf.loc[0, 1:] = [close - brick_size, close, close - brick_size, close]
        self.cdf['uptrend'] = True

        columns = ['date', 'open', 'high', 'low', 'close', 'uptrend']

        for index, row in self.df.iterrows():
            close = row['close']
            date = row['date']

            row_p1 = self.cdf.iloc[-1]
            uptrend_p1 = row_p1['uptrend']
            close_p1 = row_p1['close']

            bricks = int((close - close_p1) / brick_size)
            data = []

            state = self.get_state(close, bricks)

            print(date, bricks, close, close_p1, uptrend_p1, state)

            if state == self.UPTREND_CONTINUAL:
                uptrend = uptrend_p1
                for i in range(bricks):
                    r = [date, close_p1, close_p1 + brick_size, close_p1, close_p1 + brick_size, uptrend]
                    data.append(r)
                    close_p1 += brick_size
            elif state == self.UPTREND_REVERSAL:
                uptrend = not uptrend_p1
                bricks += 1
                close_p1 -= brick_size
                for i in range(abs(bricks)):
                    r = [date, close_p1, close_p1, close_p1 - brick_size, close_p1 - brick_size, uptrend]
                    data.append(r)
                    close_p1 -= brick_size
            elif state == self.DOWNTREND_CONTINUAL:
                for i in range(abs(bricks)):
                    r = [date, close_p1, close_p1, close_p1 - brick_size, close_p1 - brick_size, uptrend]
                    data.append(r)
                    close_p1 -= brick_size
            elif state == self.DOWNTREND_REVERSAL:
                uptrend = not uptrend_p1
                bricks -= 1
                close_p1 += brick_size
                for i in range(abs(bricks)):
                    r = [date, close_p1, close_p1 + brick_size, close_p1, close_p1 + brick_size, uptrend]
                    data.append(r)
                    close_p1 += brick_size
            else:
                continue

            sdf = pd.DataFrame(data=data, columns=columns)
            self.cdf = pd.concat([self.cdf, sdf])

        self.cdf.reset_index(inplace=True, drop=True)
        return self.cdf

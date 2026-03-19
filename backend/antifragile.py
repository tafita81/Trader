def detect_stress(df):
    vol = df['ret'].rolling(24).std()
    threshold = vol.mean() * 2
    df['stress'] = vol > threshold
    return df


def antifragile_adjustment(df, allocation):
    last = df.iloc[-1]

    if last['stress']:
        allocation = {k: v*0.5 for k,v in allocation.items()}

        for t in allocation:
            asset = df[df['ticker']==t].iloc[-1]
            if asset['zscore'] < -2:
                allocation[t] *= 1.5

    return allocation
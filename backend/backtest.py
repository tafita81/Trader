def backtest(df):
    balance = 10000
    position = 0
    history = []

    for i in range(len(df)):
        row = df.iloc[i]

        if row["buy"] and position == 0:
            position = balance / row["Close"]
            balance = 0

        elif row["sell"] and position > 0:
            balance = position * row["Close"]
            position = 0

        total = balance + position * row["Close"]
        history.append(total)

    df["equity"] = history

    return df
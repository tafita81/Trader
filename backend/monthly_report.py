# Relatório mensal estilo fundo (automático)
from datetime import datetime
import pandas as pd


def generate_monthly_report(df, capital):

    returns = df['ret'].dropna()

    sharpe = returns.mean() / (returns.std() + 1e-9)

    cumulative = (1 + returns).cumprod()

    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak

    total_return = cumulative.iloc[-1] - 1

    report = f"""
==============================
📊 RELATÓRIO MENSAL DO FUNDO
==============================

Data: {datetime.now().strftime('%Y-%m-%d')}

💰 Capital Atual: ${capital:.2f}

📈 Retorno no período: {total_return:.2%}
📊 Sharpe Ratio: {sharpe:.2f}
⚠️ Drawdown Máximo: {drawdown.min():.2%}

🧠 Resumo:
- Sistema operando automaticamente
- Estratégias evolutivas ativas
- Controle de risco aplicado

==============================
"""

    print(report)

    # salva histórico
    filename = f"reports/report_{datetime.now().strftime('%Y_%m')}.txt"

    import os
    os.makedirs("reports", exist_ok=True)

    with open(filename, "w") as f:
        f.write(report)

    return report

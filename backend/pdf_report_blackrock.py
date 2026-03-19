from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os
import yfinance as yf


def generate_blackrock_report(df, capital):

    os.makedirs("reports", exist_ok=True)

    # ===== METRICS =====
    returns = df['ret'].dropna()
    cumulative = (1 + returns).cumprod()

    sharpe = returns.mean() / (returns.std() + 1e-9)

    peak = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - peak) / peak

    total_return = cumulative.iloc[-1] - 1

    # ===== BENCHMARK =====
    sp = yf.download("^GSPC", period="1mo", interval="1d")
    sp_return = (sp["Close"].iloc[-1] / sp["Close"].iloc[0]) - 1

    # ===== GRÁFICOS =====
    plt.figure()
    plt.plot(cumulative)
    plt.title("Equity Curve")
    plt.savefig("reports/equity.png")
    plt.close()

    plt.figure()
    plt.plot(drawdown)
    plt.title("Drawdown")
    plt.savefig("reports/drawdown.png")
    plt.close()

    # ===== ANÁLISE =====
    if sharpe > 1.5:
        analysis = "Performance institucional forte e consistente."
    elif sharpe > 0:
        analysis = "Performance positiva com espaço para otimização."
    else:
        analysis = "Performance abaixo do esperado. Revisar estratégias."

    # ===== PDF =====
    doc = SimpleDocTemplate(f"reports/blackrock_report_{datetime.now().strftime('%Y_%m')}.pdf")
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Relatório de Performance do Fundo", styles['Title']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Data: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Capital: ${capital:.2f}", styles['Normal']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Retorno: {total_return:.2%}", styles['Normal']))
    content.append(Paragraph(f"Sharpe: {sharpe:.2f}", styles['Normal']))
    content.append(Paragraph(f"Drawdown: {drawdown.min():.2%}", styles['Normal']))
    content.append(Paragraph(f"Benchmark (S&P 500): {sp_return:.2%}", styles['Normal']))

    content.append(Spacer(1, 20))
    content.append(Image("reports/equity.png", width=400, height=200))

    content.append(Spacer(1, 20))
    content.append(Image("reports/drawdown.png", width=400, height=200))

    content.append(Spacer(1, 20))
    content.append(Paragraph(f"Análise: {analysis}", styles['Normal']))

    doc.build(content)

    return "Relatório BlackRock gerado"
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import numpy as np
from datetime import datetime


def generate_pdf_report(df, capital):

    doc = SimpleDocTemplate(f"reports/report_{datetime.now().strftime('%Y_%m')}.pdf")
    styles = getSampleStyleSheet()

    returns = df['ret'].dropna()
    sharpe = returns.mean() / (returns.std() + 1e-9)

    cumulative = (1 + returns).cumprod()
    peak = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - peak) / peak

    content = []

    content.append(Paragraph("Relatório Profissional do Fundo", styles['Title']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Data: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Capital: ${capital:.2f}", styles['Normal']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Sharpe Ratio: {sharpe:.2f}", styles['Normal']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Drawdown Máximo: {drawdown.min():.2%}", styles['Normal']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Retorno Total: {(cumulative.iloc[-1]-1):.2%}", styles['Normal']))

    doc.build(content)

    return "PDF gerado com sucesso"
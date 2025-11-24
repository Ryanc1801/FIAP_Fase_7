from __future__ import annotations
from dataclasses import dataclass
from typing import List
import pandas as pd


@dataclass
class Alerta:
    nivel: str
    mensagem: str
    timestamp: str


def gerar_alertas(df: pd.DataFrame) -> List[Alerta]:
    """Percorre o dataframe e gera uma lista de alertas.

    Regras simples (podem ser enriquecidas):
    - Umidade < 30 -> ATENCAO
    - Umidade < 25 -> CRITICO
    - Temperatura > 35 -> ATENCAO/CRITICO
    - pH fora da faixa [5.5, 7.0] -> ATENCAO
    """
    alertas: List[Alerta] = []

    for _, row in df.iterrows():
        ts = str(row.get("timestamp", ""))
        u = float(row["umidade"])
        t = float(row["temperatura"])
        ph = float(row["ph"])

        if u < 25:
            alertas.append(
                Alerta(
                    nivel="CRITICO",
                    mensagem=f"Umidade muito baixa ({u:.1f}%). Risco de estresse hídrico.",
                    timestamp=ts,
                )
            )
        elif u < 30:
            alertas.append(
                Alerta(
                    nivel="ATENCAO",
                    mensagem=f"Umidade baixa ({u:.1f}%). Avaliar necessidade de irrigação.",
                    timestamp=ts,
                )
            )

        if t > 37:
            alertas.append(
                Alerta(
                    nivel="CRITICO",
                    mensagem=f"Temperatura muito alta ({t:.1f}°C).",
                    timestamp=ts,
                )
            )
        elif t > 34:
            alertas.append(
                Alerta(
                    nivel="ATENCAO",
                    mensagem=f"Temperatura elevada ({t:.1f}°C). Monitorar cultura.",
                    timestamp=ts,
                )
            )

        if ph < 5.5 or ph > 7.0:
            alertas.append(
                Alerta(
                    nivel="ATENCAO",
                    mensagem=f"pH fora da faixa ideal ({ph:.1f}). Verificar correção de solo.",
                    timestamp=ts,
                )
            )

    return alertas

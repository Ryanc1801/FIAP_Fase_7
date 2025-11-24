from __future__ import annotations
from pathlib import Path
from typing import Optional
import pandas as pd
import numpy as np
import datetime as dt


COLUNAS_ESPERADAS = [
    "timestamp",
    "umidade",
    "temperatura",
    "ph",
    "nitrogenio",
    "fosforo",
    "potassio",
    "chuva_mm",
]

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sensores_demo.csv"

#Gera os dados de demonstração
def gerar_dados_aleatorios(qtd: int = 48) -> pd.DataFrame:
    base = dt.datetime.now().replace(minute=0, second=0, microsecond=0)
    registros = []

    for i in range(qtd):
        ts = base - dt.timedelta(hours=qtd - i)
        registros.append(
            {
                "timestamp": ts.strftime("%Y-%m-%d %H:%M"),
                "umidade": float(np.random.uniform(15, 70)),
                "temperatura": float(np.random.uniform(18, 38)),
                "ph": float(np.random.uniform(4.5, 7.5)),
                "nitrogenio": float(np.random.uniform(30, 80)),
                "fosforo": float(np.random.uniform(20, 60)),
                "potassio": float(np.random.uniform(25, 70)),
                "chuva_mm": float(np.random.uniform(0, 10)),
            }
        )

    return pd.DataFrame(registros)[COLUNAS_ESPERADAS].copy()

#Carrega os dados
def carregar_dados(caminho: Optional[str | Path] = None) -> pd.DataFrame:
    return gerar_dados_aleatorios()

# Salvar dataset gerado
def salvar_dados(df: pd.DataFrame, caminho: Optional[str | Path] = None) -> None:
    if caminho is None:
        caminho = DATA_PATH
    else:
        caminho = Path(caminho)

    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False)

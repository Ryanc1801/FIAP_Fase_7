from __future__ import annotations
from typing import Dict, Any
import numpy as np
import pandas as pd


def tratar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa valores ausentes e cria colunas derivadas.

    - Preenche valores ausentes com mediana
    - Cria uma coluna de faixa de umidade
    - Cria uma coluna de faixa de temperatura
    """
    df = df.copy()

    # Converte numéricos e trata NaN com mediana
    col_numericas = [
        "umidade",
        "temperatura",
        "ph",
        "nitrogenio",
        "fosforo",
        "potassio",
        "chuva_mm",
    ]
    for col in col_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        mediana = df[col].median()
        df[col] = df[col].fillna(mediana)

    # Faixas de umidade
    def classificar_umidade(u: float) -> str:
        if u < 30:
            return "Baixa"
        if u < 50:
            return "Ideal"
        return "Alta"

    # Faixas de temperatura
    def classificar_temperatura(t: float) -> str:
        if t < 20:
            return "Fria"
        if t <= 32:
            return "Confortável"
        return "Alta"

    df["faixa_umidade"] = df["umidade"].apply(classificar_umidade)
    df["faixa_temperatura"] = df["temperatura"].apply(classificar_temperatura)

    return df


def resumo_estatistico(df: pd.DataFrame) -> Dict[str, Any]:
    #Gera um dicionário com estatísticas básicas dos sensores.
    desc = df[
        [
            "umidade",
            "temperatura",
            "ph",
            "nitrogenio",
            "fosforo",
            "potassio",
            "chuva_mm",
        ]
    ].describe()

    resumo = {
        "total_registros": int(len(df)),
        "umidade_media": float(df["umidade"].mean()),
        "temperatura_media": float(df["temperatura"].mean()),
        "ph_medio": float(df["ph"].mean()),
        "tabela_descritiva": desc,
    }
    return resumo

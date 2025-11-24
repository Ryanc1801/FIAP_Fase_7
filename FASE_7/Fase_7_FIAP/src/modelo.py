from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


FEATURES = ["umidade", "temperatura", "ph", "nitrogenio", "fosforo", "potassio"]


@dataclass
class ModeloRisco:
    scaler: StandardScaler
    modelo: LogisticRegression

    def prever_risco(self, df_amostras: pd.DataFrame) -> pd.Series:
        #Retorna a classe de risco para cada amostra (BAIXO/MEDIO/ALTO)."""
        X = df_amostras[FEATURES].to_numpy()
        X_scaled = self.scaler.transform(X)
        preds = self.modelo.predict(X_scaled)
        mapeamento = {0: "BAIXO", 1: "MEDIO", 2: "ALTO"}
        return pd.Series([mapeamento[int(p)] for p in preds], index=df_amostras.index)


def _criar_rotulo_risco(df: pd.DataFrame) -> np.ndarray:
    #Cria um rótulo sintético de risco.
    risco = []
    for _, row in df.iterrows():
        score = 0.0
        if row["umidade"] < 30 or row["umidade"] > 60:
            score += 1.5
        if row["temperatura"] > 34 or row["temperatura"] < 18:
            score += 1.5
        if row["ph"] < 5.5 or row["ph"] > 7.0:
            score += 1.0
        if row["chuva_mm"] == 0 and row["umidade"] < 35:
            score += 1.0

        if score < 1.5:
            risco.append(0)  # BAIXO
        elif score < 3.0:
            risco.append(1)  # MEDIO
        else:
            risco.append(2)  # ALTO
    return np.array(risco, dtype=int)


def treinar_modelo(df: pd.DataFrame) -> ModeloRisco:
    # Treina o modelo de risco
    df = df.copy()
    y = _criar_rotulo_risco(df)
    X = df[FEATURES].to_numpy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    modelo = LogisticRegression(max_iter=500, multi_class="auto")
    modelo.fit(X_scaled, y)

    return ModeloRisco(scaler=scaler, modelo=modelo)

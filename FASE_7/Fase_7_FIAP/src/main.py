from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sensores import carregar_dados
from tratamento import tratar_dados, resumo_estatistico
from alertas import gerar_alertas, Alerta
from modelo import treinar_modelo, ModeloRisco
from aws_mensageria import enviar_alerta_sns


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Fase 7 - FarmTech Solutions | FIAP")
        self.geometry("980x640")

        self.df_bruto: pd.DataFrame | None = None
        self.df_tratado: pd.DataFrame | None = None
        self.resumo: dict | None = None
        self.alertas: list[Alerta] = []
        self.modelo_risco: ModeloRisco | None = None

        self._criar_widgets()
        self._carregar_e_processar_dados()

    # ------------------------------------------------------------------
    # Construção da interface
    # ------------------------------------------------------------------
    def _criar_widgets(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.frame_overview = ttk.Frame(notebook)
        self.frame_sensores = ttk.Frame(notebook)
        self.frame_alertas = ttk.Frame(notebook)
        self.frame_modelo = ttk.Frame(notebook)

        notebook.add(self.frame_overview, text="Visão geral")
        notebook.add(self.frame_sensores, text="Sensores")
        notebook.add(self.frame_alertas, text="Alertas")
        notebook.add(self.frame_modelo, text="Modelo de IA")

        self._build_overview_tab()
        self._build_sensores_tab()
        self._build_alertas_tab()
        self._build_modelo_tab()

    # -------------------------- ABA VISÃO GERAL ------------------------
    def _build_overview_tab(self) -> None:
        lbl = ttk.Label(
            self.frame_overview,
            text=(
                "Bem-vindo à FarmTech Solutions - Fase 7\n\n"
                "Este painel integra os principais componentes desenvolvidos ao longo do PBL:\n"
                "• Sensoriamento do campo (umidade, temperatura, pH, nutrientes)\n"
                "• Tratamento estatístico dos dados em Python\n"
                "• Geração automática de alertas de negócio\n"
                "• Estimativa de risco agronômico com Machine Learning\n"
                "• Envio de notificações em nuvem via Amazon SNS"
            ),
            justify="left",
        )
        lbl.pack(anchor="w", padx=16, pady=16)

        self.lbl_resumo = ttk.Label(self.frame_overview, text="", justify="left")
        self.lbl_resumo.pack(anchor="w", padx=16, pady=8)

        btn_recarregar = ttk.Button(
            self.frame_overview,
            text="Recarregar dados e reprocessar",
            command=self._carregar_e_processar_dados,
        )
        btn_recarregar.pack(anchor="w", padx=16, pady=8)

        # Botão para salvar os dados gerados aleatoriamente
        btn_salvar = ttk.Button(
        self.frame_overview,
        text="Salvar dados gerados",
        command=self._salvar_dados_gerados
        )
        btn_salvar.pack(anchor="w", padx=16, pady=4)


    # -------------------------- ABA SENSORES ---------------------------
    def _build_sensores_tab(self) -> None:
        cols = [
            "timestamp",
            "umidade",
            "temperatura",
            "ph",
            "nitrogenio",
            "fosforo",
            "potassio",
            "chuva_mm",
        ]
        self.tree_sensores = ttk.Treeview(
            self.frame_sensores, columns=cols, show="headings", height=15
        )
        for col in cols:
            self.tree_sensores.heading(col, text=col)
            self.tree_sensores.column(col, width=110, anchor="center")

        self.tree_sensores.pack(fill="both", expand=True, padx=8, pady=8)

    # -------------------------- ABA ALERTAS ----------------------------
    def _build_alertas_tab(self) -> None:
        self.list_alertas = tk.Listbox(self.frame_alertas, height=20)
        self.list_alertas.pack(fill="both", expand=True, padx=8, pady=8)

        btn_enviar = ttk.Button(
            self.frame_alertas,
            text="Enviar alertas CRÍTICOS por e-mail (SNS)",
            command=self._enviar_alertas_criticos,
        )
        btn_enviar.pack(anchor="e", padx=8, pady=8)

    # -------------------------- ABA MODELO -----------------------------
    def _build_modelo_tab(self) -> None:
        frame_top = ttk.Frame(self.frame_modelo)
        frame_top.pack(fill="x", padx=8, pady=8)

        ttk.Label(frame_top, text="Índice da amostra:").pack(side="left")
        self.spin_indice = tk.Spinbox(frame_top, from_=0, to=0, width=8)
        self.spin_indice.pack(side="left", padx=4)

        btn_prever = ttk.Button(
            frame_top, text="Prever risco", command=self._prever_risco_interface
        )
        btn_prever.pack(side="left", padx=4)

        self.lbl_resultado_modelo = ttk.Label(
            self.frame_modelo, text="Carregando modelo...", justify="left"
        )
        self.lbl_resultado_modelo.pack(anchor="w", padx=8, pady=8)

    # Lógica de negócios
    def _carregar_e_processar_dados(self) -> None:
        try:
            self.df_bruto = carregar_dados()
            self.df_tratado = tratar_dados(self.df_bruto)
            self.resumo = resumo_estatistico(self.df_tratado)
            self.alertas = gerar_alertas(self.df_tratado)
            self.modelo_risco = treinar_modelo(self.df_tratado)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Erro ao processar dados", str(exc))
            return

        # Atualiza aba visão geral
        texto_resumo = (
            f"Registros carregados: {self.resumo['total_registros']}\n"
            f"Umidade média: {self.resumo['umidade_media']:.1f}%\n"
            f"Temperatura média: {self.resumo['temperatura_media']:.1f} °C\n"
            f"pH médio: {self.resumo['ph_medio']:.2f}\n"
            f"Alertas gerados: {len(self.alertas)}"
        )
        self.lbl_resumo.config(text=texto_resumo)

        # Atualiza tabela de sensores
        for item in self.tree_sensores.get_children():
            self.tree_sensores.delete(item)
        for _, row in self.df_tratado.iterrows():
            valores = [
                row["timestamp"],
                f"{row['umidade']:.1f}",
                f"{row['temperatura']:.1f}",
                f"{row['ph']:.2f}",
                f"{row['nitrogenio']:.1f}",
                f"{row['fosforo']:.1f}",
                f"{row['potassio']:.1f}",
                f"{row['chuva_mm']:.1f}",
            ]
            self.tree_sensores.insert("", "end", values=valores)

        # Atualiza lista de alertas
        self.list_alertas.delete(0, tk.END)
        for alerta in self.alertas:
            self.list_alertas.insert(
                tk.END, f"[{alerta.nivel}] {alerta.timestamp} - {alerta.mensagem}"
            )

        # Atualiza spinbox de índice
        max_index = max(0, len(self.df_tratado) - 1)
        self.spin_indice.config(from_=0, to=max_index)
        self.lbl_resultado_modelo.config(
            text=(
                "Modelo treinado com sucesso.\n"
                "Selecione um índice de amostra e clique em 'Prever risco'."
            )
        )

    def _prever_risco_interface(self) -> None:
        if self.df_tratado is None or self.modelo_risco is None:
            messagebox.showwarning("Aviso", "Dados ou modelo ainda não carregados.")
            return

        try:
            idx = int(self.spin_indice.get())
        except ValueError:
            messagebox.showwarning("Aviso", "Índice inválido.")
            return

        if idx < 0 or idx >= len(self.df_tratado):
            messagebox.showwarning("Aviso", "Índice fora do intervalo.")
            return

        amostra = self.df_tratado.iloc[[idx]]
        risco = self.modelo_risco.prever_risco(amostra).iloc[0]

        texto = (
            f"Amostra #{idx}\n"
            f"Timestamp: {amostra['timestamp'].iloc[0]}\n"
            f"Umidade: {amostra['umidade'].iloc[0]:.1f}%\n"
            f"Temperatura: {amostra['temperatura'].iloc[0]:.1f} °C\n"
            f"pH: {amostra['ph'].iloc[0]:.2f}\n"
            f"Risco estimado: {risco}"
        )
        self.lbl_resultado_modelo.config(text=texto)

    def _enviar_alertas_criticos(self) -> None:
        criticos = [a for a in self.alertas if a.nivel == "CRITICO"]
        if not criticos:
            messagebox.showinfo("Alertas", "Não há alertas CRÍTICOS no momento.")
            return

        corpo = "\n".join(
            f"{a.timestamp} - {a.mensagem}"
            for a in criticos
        )

        if not messagebox.askyesno(
            "Confirmar envio",
            (
                f"Foram encontrados {len(criticos)} alertas CRÍTICOS.\n"
                "Deseja enviar um e-mail via SNS para o tópico configurado?"
            ),
        ):
            return

        try:
            enviar_alerta_sns(corpo, assunto="FarmTech - Alertas críticos de campo")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Falha ao enviar", str(exc))
        else:
            messagebox.showinfo("Sucesso", "Alertas enviados com sucesso via SNS!")

    def _salvar_dados_gerados(self) -> None:
        if self.df_bruto is None:
            messagebox.showwarning("Aviso", "Nenhum dado carregado ainda.")
            return

        from sensores import DATA_PATH

        try:
            self.df_bruto.to_csv(DATA_PATH, index=False)
            messagebox.showinfo("Sucesso", f"Dados salvos em:\n{DATA_PATH}")
        except Exception as exc:
            messagebox.showerror("Erro ao salvar", str(exc))


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

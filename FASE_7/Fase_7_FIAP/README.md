# FarmTech Solutions – Fase 7 (FIAP)

Este projeto consolida as entregas das fases anteriores do PBL em uma **única aplicação desktop**,
usando Python e Tkinter.

## Visão geral

A aplicação integra:

- **Fase 1 / 3 – Sensores**  
  Leitura (ou simulação) de dados de sensores de campo: umidade, temperatura, pH e nutrientes.

- **Fase 2 – Tratamento estatístico**  
  Limpeza de dados, criação de faixas de umidade/temperatura e resumo estatístico básico.

- **Fase 3 – Regras de negócio / alertas**  
  Geração automática de alertas de ATENÇÃO e CRÍTICO com base nas leituras.

- **Fases 5 e 6 – Machine Learning**  
  Modelo simples de classificação de risco (BAIXO / MÉDIO / ALTO) usando scikit‑learn.

- **Fase 5 – Computação em nuvem**  
  Integração com **Amazon SNS** para envio de alertas críticos por e‑mail.

Toda a lógica fica organizada em módulos dentro de `src/` e a interface gráfica
é iniciada pelo arquivo `main.py`.

## Estrutura de pastas

```text
Fase 7 - FIAP/
├── data/
│   └── sensores_demo.csv        # base de exemplo (pode ser substituída)
├── src/
│   ├── __init__.py
│   ├── aws_mensageria.py        # integração com Amazon SNS
│   ├── fase1_sensores.py        # leitura/simulação de sensores
│   ├── fase2_tratamento.py      # tratamento dos dados e estatísticas
│   ├── fase3_alertas.py         # regras de negócio e geração de alertas
│   ├── fase6_modelo.py          # modelo de risco em scikit‑learn
│   └── main.py                  # aplicação Tkinter (ponto de entrada)
├── requirements.txt
└── README.md
```

## Como executar

1. Criar e ativar um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

2. Instalar as dependências:

```bash
pip install -r requirements.txt
```

3. Definir a variável de ambiente com o ARN do tópico SNS (caso queira testar o envio de e‑mails):

```bash
# Exemplo Windows (PowerShell)
$env:FARMTECH_SNS_ARN = "arn:aws:sns:REGIAO:ID_DA_CONTA:seu-topico"

# Exemplo Linux/Mac
export FARMTECH_SNS_ARN="arn:aws:sns:REGIAO:ID_DA_CONTA:seu-topico"
```

> As credenciais da AWS devem estar configuradas via **AWS CLI** (`aws configure`)
> ou variáveis de ambiente padrão da AWS.

4. Executar a aplicação:

```bash
cd src
python main.py
```

A janela principal exibirá:

- **Visão geral** com resumo dos dados e quantidades de alertas.
- **Sensores** com tabela das leituras.
- **Alertas** com lista dos alertas ATENÇÃO/CRÍTICO e botão para envio via SNS.
- **Modelo de IA** para testar a previsão de risco (BAIXO / MÉDIO / ALTO) para qualquer registro.

## Personalização

- Você pode substituir o arquivo `data/sensores_demo.csv` pelos dados reais
  coletados no seu projeto (mantendo as mesmas colunas).
- As regras de alerta podem ser ajustadas em `fase3_alertas.py`.
- A forma de criação do rótulo de risco e o modelo podem ser refinados em
  `fase6_modelo.py` (por exemplo, trocando o algoritmo ou adicionando novos atributos).

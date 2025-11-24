# FarmTech Solutions – Fase 7 (FIAP)

Este projeto consolida as entregas das fases anteriores do PBL em uma **única aplicação desktop**,
usando Python

## Visão geral

A aplicação integra:

- **Sensores**  
  Leitura (simulação) de dados de sensores de campo: umidade, temperatura, pH e nutrientes.

- **Tratamento estatístico**  
  Limpeza de dados, criação de faixas de umidade/temperatura e resumo estatístico básico.

- **Regras de negócio / alertas**  
  Geração automática de alertas de ATENÇÃO e CRÍTICO com base nas leituras.

- **Machine Learning**  
  Modelo simples de classificação de risco (BAIXO / MÉDIO / ALTO) usando scikit‑learn.

- **Computação em nuvem**  
  Integração com **Amazon SNS** para envio de alertas críticos por e‑mail.

Toda a lógica fica organizada em módulos dentro de `src/` e a interface gráfica
é iniciada pelo arquivo `main.py`.

## Estrutura de pastas

```text
Fase_7_FIAP/
├── data/
│   └── sensores_demo.csv        # base de exemplo (pode ser substituída)
├── src/
│   ├── __init__.py
│   ├── aws_mensageria.py        # integração com Amazon SNS
│   ├── sensores.py              # leitura/simulação de sensores
│   ├── tratamento.py            # tratamento dos dados e estatísticas
│   ├── alertas.py               # regras de negócio e geração de alertas
│   ├── modelo.py                # modelo de risco em scikit‑learn
│   └── main.py                  # aplicação geral
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

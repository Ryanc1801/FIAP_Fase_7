
# 📘 **Fase 7 | FarmTech Solutions FIAP**

## **FarmTech Solutions — Fase 7 FIAP**
Integração completa das Fases 1, 2, 3, 5 e 6 em um sistema final unificado, incluindo interface gráfica, tratamento de dados, geração de alertas, modelo de Machine Learning e mensageria AWS SNS.

---

## 📌 **Descrição Geral do Projeto**
Este projeto representa o **dashboard final** do PBL de Inteligência Artificialonsolidando todas as entregas das fases anteriores em uma solução única, funcional e integrada.

A aplicação implementa:

### ✔ **Sensoriamento**
Simulação e/ou leitura de dados ambientais contendo:
- Timestamp  
- Umidade  
- Temperatura  
- pH  
- Nitrogênio  
- Fósforo  
- Potássio  
- Precipitação (chuva)

Permite:
- Carregar CSV  
- Gerar dados aleatórios para testes 
- Salvar os dados gerados

---

### ✔ **Tratamento e Estatística**
- Limpeza e padronização  
- Preenchimento de NaN com mediana  
- Criação de faixas categóricas  
- Relatório estatístico

---

### ✔ **Sistema de Alertas**
- Classificação automática  
- Alertas de atenção  
- Alertas críticos  

---

### ✔ **Mensageria (AWS SNS)**
Envio de e-mails via SNS com alertas críticas.

Configuração necessária:
```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
FARMTECH_SNS_ARN=
```

---

### ✔ **Modelo de Machine Learning**
Modelo baseado em árvore de decisão para prever risco agronômico.

---

## 📹 Vídeo da Apresentação
👉 **link do vídeo: https://youtu.be/VBxWqQFcCFs**  

---

## 👨‍💻 Autor
**Ryan Carlos**  
RM: *561677*  
Turma: *1TIAOB*

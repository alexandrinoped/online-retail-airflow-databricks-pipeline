# Pipeline de Dados com Airflow e Databricks - Online Retail

## Visão Geral
Este projeto simula um pipeline de engenharia de dados de ponta a ponta utilizando Apache Airflow e Databricks com um dataset de transações de varejo online.

O objetivo é ingerir dados brutos em CSV, aplicar transformações e regras de negócio, e disponibilizar tabelas analíticas organizadas em uma arquitetura em camadas no padrão medallion:

- Bronze: dados brutos ingeridos
- Silver: dados tratados e padronizados
- Gold: dados analíticos prontos para consumo

## Objetivos do Projeto
- Construir um pipeline orquestrado com Airflow
- Processar dados no Databricks com Spark
- Organizar os dados em camadas Bronze, Silver e Gold
- Aplicar regras de negócio e padronização dos dados
- Entregar saídas analíticas com foco em uso de negócio

## Arquitetura

```text
Fonte CSV (Kaggle)
    ↓
Upload do arquivo para o Databricks Workspace
    ↓
Notebook Bronze no Databricks
    ↓
Notebook Silver no Databricks
    ↓
Notebook Gold no Databricks
    ↓
Tabelas Delta para consumo analítico

Orquestração

O Apache Airflow é responsável por orquestrar a execução do pipeline.

Processamento

O Databricks é responsável por executar as transformações em Spark e persistir as camadas Bronze, Silver e Gold.

Execução do Pipeline

O Airflow dispara um Job no Databricks, que executa as etapas em sequência:

Bronze
Silver
Gold
Dataset

O dataset contém registros transacionais de varejo online, com colunas como:

Invoice / InvoiceNo
StockCode
Description
Quantity
InvoiceDate
Price / UnitPrice
Customer ID / CustomerID
Country
Regras de Negócio
Quantity > 0 e UnitPrice > 0: venda válida
Quantity < 0: devolução
InvoiceNo iniciando com "C": cancelamento
CustomerID nulo: cliente não identificado
Description nula: item inconsistente
total_amount = Quantity * UnitPrice
Camadas do Pipeline
Bronze

A camada Bronze realiza a ingestão do arquivo CSV bruto, adicionando metadados técnicos como:

ingestion_timestamp
source_file

Saída gerada:

default.bronze_online_retail_raw
Silver

A camada Silver realiza:

padronização de tipos
tratamento de preço com vírgula decimal
criação da coluna total_amount
classificação dos registros em:
Sale
Return
Cancelled
Invalid
identificação de cliente e item

Saída gerada:

default.silver_online_retail_clean
Gold

A camada Gold gera três tabelas analíticas:

default.gold_fact_sales

Tabela fato contendo apenas transações classificadas como venda válida.

default.gold_dim_customer

Tabela dimensional de clientes com:

primeira compra
última compra
total de pedidos
receita total
default.gold_agg_rfm_customer

Tabela analítica com métricas de:

Recência
Frequência
Monetização

Estrutura do Projeto

online-retail-airflow-databricks-pipeline/
│
├── README.md
├── requirements.txt
├── .gitignore
├── dags/
│   └── online_retail_pipeline_dag.py
├── notebooks/
│   ├── 01_bronze_ingestion.py
│   ├── 02_silver_transformation.py
│   └── 03_gold_modeling.py
├── src/
│   ├── config.py
│   ├── utils.py
│   └── quality_checks.py
├── docs/
│   ├── architecture.md
│   ├── business_rules.md
│   └── data_dictionary.md
└── data/
    └── raw/

Papel de Cada Componente
dags/

Contém a DAG do Airflow responsável por disparar o Job do Databricks.

notebooks/

Contém a lógica das etapas Bronze, Silver e Gold adaptadas para execução no Databricks.

docs/

Contém a documentação complementar do projeto:

arquitetura
regras de negócio
dicionário de dados
src/

Mantido como apoio de desenvolvimento e organização inicial do projeto. A execução principal do pipeline ocorre no Databricks, por meio dos notebooks Bronze, Silver e Gold.

data/raw/

Mantido como referência local do arquivo de origem utilizado no projeto.

Stack Utilizada
Python
PySpark
Apache Airflow
Databricks
Delta Lake
Arquitetura Medallion
Orquestração com Airflow

A DAG no Airflow utiliza o operador DatabricksRunNowOperator para disparar o Job criado no Databricks.

Com isso:

o Airflow não processa os dados diretamente
o Airflow coordena a execução
o Databricks executa o pipeline
Resultado Final

O projeto foi executado com sucesso com a seguinte arquitetura:

Airflow disparando o pipeline
Databricks executando Bronze, Silver e Gold
tabelas analíticas persistidas no Databricks em formato Delta
Próximas Evoluções
parametrização do pipeline
ingestão incremental
testes automatizados de qualidade
monitoramento e alertas
integração com storage em nuvem
evolução para catálogos e governança mais robusta
# Arquitetura

Este projeto segue uma arquitetura em camadas inspirada no padrão medallion.

## Fluxo
CSV bruto → Bronze → Silver → Gold

## Componentes

### Fonte
Dataset em CSV armazenado na pasta `data/raw`.

### Airflow
Responsável pela orquestração do pipeline, controle de dependências entre tarefas, tentativas de reexecução e agendamento.

### Databricks
Responsável pela leitura, transformação, validação e persistência dos dados em cada camada.

## Camadas

### Bronze
Armazena os dados brutos ingeridos, com metadados técnicos e mínimas alterações.

### Silver
Contém os dados tratados, padronizados e classificados de acordo com regras de negócio.

### Gold
Contém os dados analíticos prontos para consumo, consulta e geração de insights.
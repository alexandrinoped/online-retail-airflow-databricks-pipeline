# Dicionário de Dados

| Coluna       | Descrição |
|--------------|-----------|
| InvoiceNo    | Identificador da fatura/transação |
| StockCode    | Código do produto/item |
| Description  | Descrição do produto |
| Quantity     | Quantidade comprada ou devolvida |
| InvoiceDate  | Data e hora da transação |
| UnitPrice    | Preço unitário do item |
| CustomerID   | Identificador do cliente |
| Country      | País do cliente |

## Colunas Derivadas

| Coluna              | Descrição |
|---------------------|-----------|
| ingestion_timestamp | Data e hora da ingestão do dado bruto |
| source_file         | Nome do arquivo de origem |
| total_amount        | Valor total da linha (`Quantity * UnitPrice`) |
| invoice_status      | Classificação do registro: Sale / Return / Cancelled / Invalid |
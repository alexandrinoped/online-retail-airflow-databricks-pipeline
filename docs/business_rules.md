# Regras de Negócio

## Classificação dos Registros

### Venda Válida
Um registro é considerado uma venda válida quando:
- `Quantity > 0`
- `UnitPrice > 0`
- `InvoiceNo` não começa com `"C"`

### Devolução
Um registro é classificado como devolução quando:
- `Quantity < 0`

### Cancelamento
Um registro é classificado como cancelamento quando:
- `InvoiceNo` começa com `"C"`

### Cliente Não Identificado
Um registro é marcado como cliente não identificado quando:
- `CustomerID` é nulo

### Item Inconsistente
Um registro é marcado como item inconsistente quando:
- `Description` é nula

## Campos Derivados

### total_amount
Campo calculado como:

`Quantity * UnitPrice`

### invoice_status
Classificação final do registro:
- `Sale`
- `Return`
- `Cancelled`
- `Invalid`

### customer_status
Classificação do cliente:
- `Identified`
- `Unidentified`

### item_status
Classificação do item:
- `Valid`
- `Inconsistent`
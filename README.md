# dio-live-textract2
Repositório de código para o live coding do dia 05/10/2021 sobre extração de dados estruturados e gravação em banco de dados a partir do Amazon Textract.

## Serviços utilizados

- Amazon Textract
- AWS Lambda
- Amazon S3
- Amazon DynamoDB

## Desenvolvimento

### Criando um bucket no Amazon S3

- S3 Console -> Create bucket -> Bucket name "dio-live-input-data" -> Manter as configurações padrão -> Create bucket

### Processando imagens no Amazon Textract

- Textract Console -> Select Document -> Analyze Document -> Tables
- Download results -> Salvar arquivo _.zip_

### Criando uma tabela no DynamoDB

- DynamoDB Console -> Tables -> Create Table -> Partition key "Indice" -> Create table

### Implementando a função lambda

- Lambda Console -> Functions -> Create function
- Use a blueprint -> "s3-get-object-python"
- Function name "dio-live-csv-to-db"
- Execution role -> "Create a new role from AWS policy templates" -> Role name "S3ToDynamoDBRole"
- S3 Trigger -> Bucket criado anteriormente
- Create function
- Substituir o código gerado pelo código da pasta ```/src``` deste repositório (Obs: atenção para o nome da tabela, deve ser substituído pelo nome da sua)

#### Passo adicional: Criando um layer com a biblioteca boto3 do Python

- Lambda Console -> Additional Resources -> Layers

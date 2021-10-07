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

- DynamoDB Console -> Tables -> Create Table -> Partition key "cod" -> Create table

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
- Name "boto3_layer" -> Upload a .zip file -> baixe e insira o arquivo ```.zip``` contido na pasta ```/src``` deste respositório
- Compatible architecture "x86_64"
- Compatible runtimes "Python3.7" (É necessário ser Python3.7 para ser compatível com a versão do blueprint utilizado)
- Create
- Na função lambda criada -> Selecione layers no diagrama -> Add layer -> Custom layers "boto3_layer" -> Version 1 -> Add

### Configurando permissões no Lambda para o DynamoDB

- Lambda Console -> Functions -> Selecione a função criada -> Configuration -> Permission -> Execution Role -> Abrir a role criada no Amazon IAM
- No IAM -> Permission -> Add inline policy -> Choose a service "DynamoDB" -> Write "PutItem"
- Resources -> Selecionar o Arn da sua tabela -> Selecionar a sua região -> Add -> Review Policy -> Name "LambdaDynamoDBPolicy" -> Create policy

## Utilizando a aplicação

### No Amazon Textract

- Amazon Textract Console -> Select Document -> Choose file -> Buscar o arquivo a ser analisado
- Download results  

## No Amazon S3

- Extrair o arquivo ```table_1.csv``` do arquivo baixado do Amazon Textract
- Acessar o bucket criado anteriormente -> Upload -> Selecionar o arquivo ```table_1.csv``` -> Upload

## No DynamoDB

- Tables -> Acessar a tabela criada -> View Items

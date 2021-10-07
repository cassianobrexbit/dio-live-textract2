import json
import boto3

# instanciar serviços da AWS com a biblioteca boto3
s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

# declarar a tabela do DynamoDB de destino
invoice_table = dynamodb.Table("nome_da_tabela")

def lambda_handler(event, context):
    
    # obter o nome do bucket de origem do arquivo
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    
    # obter o nome do arquivo a ser processado
    file_name = event['Records'][0]['s3']['object']['key']
    
    # buscar no bucket S3 o arquivo a ser processado
    file_object = s3_client.get_object(Bucket = source_bucket, Key = file_name)
    
    # extrair o conteúdo do arquivo obtido
    file_content = file_object['Body'].read().decode("utf-8")
    
    # cria uma lista e cada índice da lista é delimitado por uma quebra de linha
    orders = file_content.split("\n")
    
    # varre a lista desprezando o primeiro índice (cabeçalho) e o último (nesse caso é item vazio) inserindo os itens no DynamoDB
    for order in orders[1:-1]:
        
        # uma segunda lista é criada com os itens da linha, delimitados pelo caracter da vírgula
        data = order.split(",")
        
        # atribui os itens da lista às variáveis que serão registradas no DynamoDB
        cod = data[0]
        item = data[1]
        quantidade = data[2]
        unMed = data[3]
        valorUn = data[4]
        valorTotal = data[5]
        
        # envia o item para o DynamoDB
        invoice_table.put_item(
        Item = {
            "cod" : cod.replace('"', ""),
            "item" : item.replace('"', ""),
            "quantidade" : quantidade.replace('"', ""),
            "unMed" : unMed.replace('"', ""),
            "valorUn" : valorUn.replace('"', ""),
            "valorTotal": valorTotal.replace('"', "")
        }
        )
        

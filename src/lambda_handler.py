import json
import boto3
import os
import csv
import codecs
import sys
import urllib.parse

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
tableName = "nome_da_tabela"


def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    

    #get() does not store in memory
    try:
        obj = s3.Object(bucket, key).get()['Body']
    except:
        print('Falha ao obter arquivo do S3')
    try:
        table = dynamodb.Table(tableName)
    except:
        print('Falha ao acessar a tabela no DynamoDB')

    batch_size = 100
    batch = []

    #DictReader is a generator; not stored in memory
    for row in csv.DictReader(codecs.getreader('utf-8')(obj)):
        if len(batch) >= batch_size:
            write_to_dynamo(batch)
            batch.clear()

        batch.append(row)

    if batch:
        write_to_dynamo(batch)

    return {
        'statusCode': 200,
        'body': json.dumps('Dados enviados ao DynamoDB')
    }

    
def write_to_dynamo(rows):
    try:
        table = dynamodb.Table(tableName)
    except:
        print('Falha ao acessar tabela no DynamoDB')

    try:
        with table.batch_writer() as batch:
            for i in range(len(rows)):
                batch.put_item(
                Item=rows[i]
            )
    except Exception as e:
        print('Erro ao executar inserção dos dados no DynamoDB')
        print(e)

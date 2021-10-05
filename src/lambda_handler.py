import json
import boto3
import os
import csv
import codecs
import sys
import urllib.parse
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
tableName = "DIOTableTest"


def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    

    #get() does not store in memory
    try:
        obj = s3.Object(bucket, key).get()['Body']
    except:
        print('S3 Object could not be opened ')
    try:
        table = dynamodb.Table(tableName)
    except:
        print('Error loading DynamoDB table')

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
        'body': json.dumps('Uploaded to DynamoDB Table')
    }

    
def write_to_dynamo(rows):
    try:
        table = dynamodb.Table(tableName)
    except:
        print('Falha ao identificar a tabela do DynamoDB')

    try:
        with table.batch_writer() as batch:
            for i in range(len(rows)):
                batch.put_item(
                Item=rows[i]
            )
    except Exception as e:
        print('Error executing batch_writer')
        print(e)

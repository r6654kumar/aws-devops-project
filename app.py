import boto3
import pymysql
import os

# AWS clients
s3 = boto3.client('s3')
glue = boto3.client('glue')

# Database connection details
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def read_from_s3(bucket_name, file_key):
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    return response['Body'].read().decode('utf-8')

def push_to_rds(data):
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO table_name (column_name) VALUES (%s)", (data,))
            connection.commit()
        return True
    except Exception as e:
        print(f"Error pushing to RDS: {e}")
        return False

def push_to_glue(data):
    try:
        response = glue.put_data(
            DatabaseName='glue_database_name',
            TableName='glue_table_name',
            Data=data
        )
        print("Data pushed to Glue successfully.")
    except Exception as e:
        print(f"Error pushing to Glue: {e}")

def handler(event, context):
    bucket_name = event['bucket_name']
    file_key = event['file_key']

    data = read_from_s3(bucket_name, file_key)

    if not push_to_rds(data):
        push_to_glue(data)



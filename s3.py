import boto3
import pandas as pd
import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Leer las variables de entorno
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

s3 = boto3.client(
   's3',
   region_name='us-east-1',
   aws_access_key_id=ACCESS_KEY,
   aws_secret_access_key=SECRET_KEY)

bucket_name = 'grupo-4-mlops'
file_name = 'advertiser_ids'

file_object = s3.get_object(Bucket=bucket_name, Key=file_name)
df = pd.read_csv(file_object['Body'])
print(df)
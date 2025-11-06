import os
import boto3

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")

aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

bucket_name = "aimodeler-demo-llm-documents"

download_dir = 'documents'
os.makedirs(download_dir, exist_ok=True)

s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

response = s3.list_objects_v2(Bucket=bucket_name)

if 'Contents' in response:
    for obj in response['Contents']:
        key = obj['Key']
        filename = os.path.basename(key)
        local_path = os.path.join(download_dir, filename)
        print(f"Downloading: {key} -> {local_path}")
        s3.download_file(bucket_name, key, local_path)
else:
    print("No files found in the bucket.")

import os
import openai
import tiktoken

openai.api_key = os.getenv("OPENAI_API_KEY")

LLM_MODEL="gpt-4o"

TOKENIZER = tiktoken.encoding_for_model("text-embedding-3-small")

EMBED_MODEL="text-embedding-3-small"

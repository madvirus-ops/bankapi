import boto3
import uuid
import botocore
import boto3.s3.transfer as s3transfer
from typing import List
from dotenv import load_dotenv
load_dotenv()
import os 


aws_public_key = os.getenv("AWS_PUBLIC_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")
region_name = os.getenv("AWS_REGION")
bucket = os.getenv("BUCKET")


class UploadWorker:

    @staticmethod
    def upload_file(file,user:dict,upload_type:str) -> List[dict]:
        try:
            folder = (user.username if user.username is not None else uuid.uuid4().hex[:6])
            botoconfig = botocore.config.Config(max_pool_connections=10)
            s3client = boto3.Session.client(
                's3',aws_access_key_id=aws_public_key,
                aws_secret_access_key=aws_secret_key,
                region_name=region_name,
                config=botoconfig
            )
            transfer_config = s3transfer.TransferConfig(use_threads=True,max_concurrency=10)
            ext = file.name[file.name.rfind(".") :].lower()

            s3_slave = s3transfer.create_transfer_manager(s3client,transfer_config)
            key = f"{upload_type}/{folder}/{uuid.uuid4().hex[:6]}{ext}"

            s3_slave.upload(file,bucket,key,extra_args={"ACL":"public-read"})

            public_url = f"https://{bucket}.s3.amazonaws.com/{key}"

            response = {
                "status":"success","code":200,
                "message":"upload In Progress",
                "file_url":key,"public_url":public_url
            }
            return response

        except Exception as e:
            print(e.args)
            return {
                "status":"error","code":400,
                "message":"Upload failed",
                "reason":e.args
            }

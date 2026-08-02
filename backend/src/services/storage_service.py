import os
import uuid
from abc import ABC, abstractmethod
from werkzeug.utils import secure_filename
from flask import current_app


class StorageAdapter(ABC):
    @abstractmethod
    def upload_file(self, file_storage, folder: str) -> str:
        pass


class LocalStorageAdapter(StorageAdapter):
    def __init__(self, base_path: str):
        self.base_path = base_path

    def upload_file(self, file_storage, folder: str) -> str:
        folder_path = os.path.join(self.base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        original_filename = secure_filename(file_storage.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        file_path = os.path.join(folder_path, unique_filename)

        file_storage.save(file_path)

        relative_url = f"/static/uploads/{folder}/{unique_filename}"
        return relative_url


class S3StorageAdapter(StorageAdapter):
    def __init__(self, s3_client, bucket_name: str, region: str):
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.region = region

    def upload_file(self, file_storage, folder: str) -> str:
        original_filename = secure_filename(file_storage.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        s3_key = f"{folder}/{unique_filename}"

        self.s3_client.upload_fileobj(
            file_storage,
            self.bucket_name,
            s3_key,
            ExtraArgs={'ACL': 'public-read'}
        )

        public_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"
        return public_url


class StorageService:
    _adapter: StorageAdapter = None

    @classmethod
    def _get_adapter(cls) -> StorageAdapter:
        if cls._adapter is not None:
            return cls._adapter

        provider = os.getenv('STORAGE_PROVIDER', 'local').lower()

        if provider == 's3':
            import boto3
            aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
            aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
            aws_region = os.getenv('AWS_REGION', 'us-east-1')
            bucket_name = os.getenv('S3_BUCKET_NAME', '')

            s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region
            )
            cls._adapter = S3StorageAdapter(s3_client, bucket_name, aws_region)
        else:
            services_dir = os.path.dirname(os.path.abspath(__file__))
            src_dir = os.path.dirname(services_dir)
            base_upload_path = os.path.join(src_dir, 'static', 'uploads')
            cls._adapter = LocalStorageAdapter(base_upload_path)

        return cls._adapter

    @classmethod
    def upload_file(cls, file_storage, folder: str = 'default') -> str:
        if file_storage is None or not file_storage.filename:
            raise ValueError('No se proporcionó un archivo válido')

        adapter = cls._get_adapter()
        return adapter.upload_file(file_storage, folder)

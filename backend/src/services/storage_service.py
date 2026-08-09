# src/services/storage_service.py
import os
import uuid
from abc import ABC, abstractmethod
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'doc', 'txt', 'md'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class StorageAdapter(ABC):
    @abstractmethod
    def upload_file(self, file_storage, folder: str) -> str:
        pass

    @abstractmethod
    def download_file(self, file_path: str) -> str:
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        pass


class LocalStorageAdapter(StorageAdapter):
    def __init__(self, base_path: str):
        self.base_path = base_path  # Apunta directamente a .../src/static/uploads

    def upload_file(self, file_storage, folder: str) -> str:
        folder_path = os.path.join(self.base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        original_filename = secure_filename(file_storage.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        file_path = os.path.join(folder_path, unique_filename)

        file_storage.save(file_path)

        relative_url = f"/static/uploads/{folder}/{unique_filename}"
        return relative_url

    def download_file(self, file_path: str) -> str:
        # Si por alguna razón ya contiene una URL completa (ej. S3), se retorna directo
        if file_path.startswith('http://') or file_path.startswith('https://'):
            return file_path

        # Limpia la ruta relativa y la une correctamente con base_path
        clean_path = file_path.replace('/static/uploads/', '').lstrip('/')
        full_path = os.path.join(self.base_path, clean_path)

        if not os.path.exists(full_path):
            raise ValueError("El archivo no existe en el disco")
        return full_path

    def delete_file(self, file_path: str) -> bool:
        try:
            if file_path.startswith('http://') or file_path.startswith('https://'):
                return True
            
            clean_path = file_path.replace('/static/uploads/', '').lstrip('/')
            full_path = os.path.join(self.base_path, clean_path)

            if os.path.exists(full_path):
                os.remove(full_path)
                return True
            return False
        except Exception:
            return False


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
            s3_key
        )

        public_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"
        return public_url

    def download_file(self, file_path: str) -> str:
        s3_key = file_path.split(f".amazonaws.com/")[-1]
        url = self.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': s3_key},
            ExpiresIn=3600
        )
        return url

    def delete_file(self, file_path: str) -> bool:
        try:
            s3_key = file_path.split(f".amazonaws.com/")[-1]
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except Exception:
            return False


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

        if not allowed_file(file_storage.filename):
            raise ValueError('Tipo de archivo no permitido')

        adapter = cls._get_adapter()
        return adapter.upload_file(file_storage, folder)

    @classmethod
    def download_file(cls, file_path: str) -> str:
        adapter = cls._get_adapter()
        return adapter.download_file(file_path)

    @classmethod
    def delete_file(cls, file_path: str) -> bool:
        adapter = cls._get_adapter()
        return adapter.delete_file(file_path)
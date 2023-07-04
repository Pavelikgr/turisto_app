import os
from fastapi import UploadFile

class AvatarStorage:
    def __init__(self, storage_directory: str):
        self.storage_directory = storage_directory

    def save_avatar(self, file: UploadFile, filename: str):
        file_path = os.path.join(self.storage_directory, filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

    def delete_avatar(self, filename: str):
        file_path = os.path.join(self.storage_directory, filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    def get_avatar_path(self, filename: str) -> str:
        return os.path.join(self.storage_directory, filename)

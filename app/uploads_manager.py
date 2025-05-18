import os
from pathlib import Path


class UploadsManager:
    def __init__(self, uploads_dir_path: str = "uploads"):
        try:
            os.mkdir(uploads_dir_path)
        except FileExistsError:
            pass
    
    def create_dir(self, path: str):
        os.mkdir(path)
import os
from pathlib import Path


class UploadsManager:
    def __init__(self):
        try:
            os.mkdir("uploads/")
        except FileExistsError:
            pass
    
    def create_or_update_file(self, filename: str, content: bytes):
        with open(f"uploads/{filename}", 'wb') as f:
            f.write(content)

    def remove_file(self, filename: str):
        os.remove(f"uploads/{filename}")
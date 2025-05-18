import pytest
import os
from pathlib import Path
from app.uploads_manager import UploadsManager


def test_constructor():
    uploads_manager = UploadsManager()
    assert os.path.isdir("uploads") == True

def test_create_or_update_file():
    uploads_manager = UploadsManager()
    current_dir = Path(__file__).parent.parent
    test_file_path = current_dir / "resources" / "test_file.txt"
    
    with open(test_file_path, "rb") as f:
        content = f.read()
    uploads_manager.create_or_update_file("test", content)
    
    with open("uploads/test", "rb") as f:
        data = f.read()
    
    assert os.path.exists("uploads/test")
    assert content == data
    
    os.remove("uploads/test")

def test_remove_file():
    open("uploads/new_dir", 'a').close()
    uploads_manager = UploadsManager()
    uploads_manager.remove_file("new_dir")
    
    assert os.path.exists("uploads/new_dir") == False
    
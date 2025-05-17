import pytest
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from app.models import User
from app.schemas import ItemCreate
from app.crud.item import *

@pytest.fixture
def sample_item_data():
    return ItemCreate(
        name="test_file.txt",
        is_dir=False,
        parent_id=None,
        size=1024,
        mimetype="text/plain",
        parent=None
    )

@pytest.fixture(autouse=True)
def clear_items_table(test_db):
    test_db.execute(delete(Item))
    test_db.commit()

def test_create_item(test_db, sample_item_data):
    item = create_item(test_db, sample_item_data)
    assert item.id is not None
    assert item.name == sample_item_data.name
    assert item.is_dir == sample_item_data.is_dir
    assert item.path == "uploads/test_file.txt"

def test_read_item(test_db, sample_item_data):
    created = create_item(test_db, sample_item_data)
    read = read_item(test_db, created.id)
    assert read is not None
    assert read.id == created.id

def test_read_item_not_found(test_db):
    read = read_item(test_db, 999999)  # some non-existing ID
    assert read is None

def test_read_all_items(test_db, sample_item_data):
    # Ensure clean slate
    for item in read_all_items(test_db):
        test_db.delete(item)
    test_db.commit()

    # Add items
    create_item(test_db, sample_item_data)
    create_item(test_db, ItemCreate(
        name="test_file2.txt",
        is_dir=False,
        parent_id=None,
        size=1024,
        mimetype="text/plain",
        parent=None
    ))

    items = read_all_items(test_db)
    assert isinstance(items, list)
    assert len(items) >= 2

def test_create_item_duplicate(test_db, sample_item_data):
    create_item(test_db, sample_item_data)
    # If your test_db schema enforces uniqueness (e.g. unique path), try duplicating and expect error
    with pytest.raises(IntegrityError):
        create_item(test_db, sample_item_data)

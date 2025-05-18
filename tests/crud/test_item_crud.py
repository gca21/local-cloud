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
    with pytest.raises(IntegrityError):
        create_item(test_db, sample_item_data)

def create_item_helper(db: Session, **kwargs) -> Item:
    item = Item(**kwargs)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def test_update_item_name(test_db: Session):
    item = create_item_helper(test_db, name="old.txt", is_dir=False, path="uploads/old.txt")
    update_data = ItemUpdate(id=item.id, name="new.txt")
    
    updated = update_item(test_db, update_data)
    
    assert updated.name == "new.txt"
    assert updated.path == "uploads/old.txt"  # path doesn't change unless parent changes

def test_update_item_parent(test_db: Session):
    parent = create_item_helper(test_db, name="dir", is_dir=True, path="uploads/dir")
    item = create_item_helper(test_db, name="file.txt", is_dir=False, path="uploads/file.txt")
    
    update_data = ItemUpdate(id=item.id, parent_id=parent.id)
    updated = update_item(test_db, update_data)
    
    assert updated.parent_id == parent.id
    assert updated.path == build_path(test_db, updated.name, updated.parent_id)

def test_update_name_and_parent(test_db: Session):
    parent = create_item_helper(test_db, name="dir", is_dir=True, path="uploads/dir")
    item = create_item_helper(test_db, name="file.txt", is_dir=False, path="uploads/file.txt")
    
    update_data = ItemUpdate(id=item.id, name="renamed.txt", parent_id=parent.id)
    updated = update_item(test_db, update_data)
    
    assert updated.name == "renamed.txt"
    assert updated.parent_id == parent.id
    assert updated.path == build_path(test_db, "renamed.txt", parent.id)

def test_update_nonexistent_item(test_db: Session):
    update_data = ItemUpdate(id="999", name="newname.txt")
    result = update_item(test_db, update_data)
    assert result is None

def test_update_with_invalid_parent(test_db: Session):
    item = create_item_helper(test_db, name="file.txt", is_dir=False, path="uploads/file.txt")
    update_data = ItemUpdate(id=item.id, parent_id="999")  # Non-existent parent
    
    result = update_item(test_db, update_data)
    assert result is None

def test_update_directory_updates_children_paths(test_db: Session):
    parent = create_item_helper(test_db, name="old_dir", is_dir=True, path="uploads/old_dir")
    child = create_item_helper(test_db, name="child.txt", is_dir=False, path="uploads/old_dir/child.txt", parent_id=parent.id)

    new_parent = create_item_helper(test_db, name="new_dir", is_dir=True, path="uploads/new_dir")
    
    update_data = ItemUpdate(id=parent.id, parent_id=new_parent.id)
    updated = update_item(test_db, update_data)

    assert updated.parent_id == new_parent.id
    assert updated.path == build_path(test_db, parent.name, new_parent.id)

    test_db.refresh(child)
    expected_child_path = build_path(test_db, child.name, updated.id)
    assert child.path == expected_child_path

def test_delete_existing_item(test_db: Session):
    # Create an item first
    item = create_item_helper(test_db, name="to_delete.txt", is_dir=False, path="uploads/to_delete.txt")
    
    # Delete the item
    deleted = delete_item(test_db, item.id)
    
    # Confirm the returned item is the same
    assert deleted is not None
    assert deleted.id == item.id
    
    # Confirm the item is actually deleted from DB
    should_be_none = test_db.get(Item, item.id)
    assert should_be_none is None

def test_delete_nonexistent_item(test_db: Session):
    # Try deleting an item with a non-existent id
    deleted = delete_item(test_db, 999999)
    
    # Should return None
    assert deleted is None


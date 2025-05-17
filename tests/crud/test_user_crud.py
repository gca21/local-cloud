import pytest
from sqlalchemy.exc import IntegrityError
from app.models import User
from app.crud.user import *


def test_username_exists_returns_true(test_db):
    user = User(username="alice", password="hashed123")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    assert username_exists(test_db, "alice") is True

def test_username_exists_returns_false(test_db):
    assert username_exists(test_db, "nonexistent") is False

def test_read_user_returns_user_if_exists(test_db):
    # Arrange
    user = User(username="bob", password="hashedpw")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    # Act
    retrieved = read_user(test_db, user.id)

    # Assert
    assert retrieved is not None
    assert retrieved.id == user.id
    assert retrieved.username == "bob"

def test_create_user_success(test_db):
    user = create_user(test_db, "testuser", "hashedpw123")
    assert user.id is not None
    assert user.username == "testuser"
    assert user.password == "hashedpw123"

def test_create_user_raises_integrity_error_on_duplicate(test_db):
    # Create first user
    user1 = create_user(test_db, "duplicateuser", "pw1")
    assert user1.id is not None

    # Attempt to create duplicate username triggers IntegrityError
    with pytest.raises(IntegrityError):
        create_user(test_db, "duplicateuser", "pw2")

def test_update_user_success(test_db):
    # Create initial user
    user = create_user(test_db, "originaluser", "originalpw")
    
    # Update username and password
    updated_user = update_user(test_db, user.id, username="newuser", hashed_password="newpw")
    assert updated_user is not None
    assert updated_user.id == user.id
    assert updated_user.username == "newuser"
    assert updated_user.password == "newpw"

def test_update_user_partial_update(test_db):
    user = create_user(test_db, "partialuser", "pw1")
    
    # Update only username
    updated_user = update_user(test_db, user.id, username="updateduser")
    assert updated_user.username == "updateduser"
    assert updated_user.password == "pw1"
    
    # Update only password
    updated_user = update_user(test_db, user.id, hashed_password="pw2")
    assert updated_user.username == "updateduser"
    assert updated_user.password == "pw2"

def test_update_user_not_found_returns_none(test_db):
    updated_user = update_user(test_db, 9999, username="doesnotexist")
    assert updated_user is None

def test_update_user_raises_integrity_error_on_duplicate_username(test_db):
    user1 = create_user(test_db, "user1", "pw1")
    user2 = create_user(test_db, "user2", "pw2")
    
    with pytest.raises(IntegrityError):
        update_user(test_db, user2.id, username="user1")  # user1's username already taken

def test_delete_existing_user_returns_user(test_db):
    user = create_user(test_db, "deleteuser", "pw")
    deleted_user = delete_user(test_db, user.id)
    assert deleted_user is not None
    assert deleted_user.id == user.id
    assert deleted_user.username == "deleteuser"

def test_delete_nonexistent_user_returns_none(test_db):
    deleted_user = delete_user(test_db, 9999)
    assert deleted_user is None

def test_delete_removes_user_from_db(test_db):
    user = create_user(test_db, "tobedeleted", "pw")
    deleted_user = delete_user(test_db, user.id)
    assert deleted_user is not None

    # Confirm user no longer exists
    fetched = read_user(test_db, user.id)
    assert fetched is None
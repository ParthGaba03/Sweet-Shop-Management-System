import pytest
from fastapi import status

def test_register_user(client, db):
    """Test user registration"""
    response = client.post("/api/auth/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword123"
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "newuser"
    assert data["user"]["email"] == "newuser@example.com"
    assert data["user"]["role"] == "user"

def test_register_duplicate_username(client, db, test_user):
    """Test registration with duplicate username"""
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "different@example.com",
        "password": "password123"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_register_duplicate_email(client, db, test_user):
    """Test registration with duplicate email"""
    response = client.post("/api/auth/register", json={
        "username": "differentuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_login_success(client, db, test_user):
    """Test successful login"""
    response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "testuser"

def test_login_invalid_username(client, db):
    """Test login with invalid username"""
    response = client.post("/api/auth/login", data={
        "username": "nonexistent",
        "password": "password123"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_login_invalid_password(client, db, test_user):
    """Test login with invalid password"""
    response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


import pytest
from fastapi import status
from decimal import Decimal
from app.models import Sweet

def test_create_sweet_as_admin(client, admin_token, db):
    """Test creating a sweet as admin"""
    response = client.post(
        "/api/sweets",
        json={
            "name": "Chocolate Bar",
            "category": "Chocolate",
            "price": "5.99",
            "quantity": 50
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Chocolate Bar"
    assert data["category"] == "Chocolate"
    assert float(data["price"]) == 5.99
    assert data["quantity"] == 50

def test_create_sweet_as_user_unauthorized(client, auth_token, db):
    """Test that regular users cannot create sweets"""
    response = client.post(
        "/api/sweets",
        json={
            "name": "Chocolate Bar",
            "category": "Chocolate",
            "price": "5.99",
            "quantity": 50
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_create_sweet_unauthorized(client, db):
    """Test creating sweet without authentication"""
    response = client.post(
        "/api/sweets",
        json={
            "name": "Chocolate Bar",
            "category": "Chocolate",
            "price": "5.99",
            "quantity": 50
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_all_sweets(client, auth_token, db):
    """Test getting all sweets"""
    # Create a sweet first (manually since we need admin)
    sweet = Sweet(
        name="Test Sweet",
        category="Test",
        price=Decimal("10.00"),
        quantity=20
    )
    db.add(sweet)
    db.commit()
    db.refresh(sweet)
    
    response = client.get(
        "/api/sweets",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Sweet"

def test_search_sweets_by_name(client, auth_token, db):
    """Test searching sweets by name"""
    sweet1 = Sweet(name="Chocolate Bar", category="Chocolate", price=Decimal("5.99"), quantity=10)
    sweet2 = Sweet(name="Gummy Bears", category="Candy", price=Decimal("3.99"), quantity=20)
    db.add_all([sweet1, sweet2])
    db.commit()
    
    response = client.get(
        "/api/sweets/search?name=Chocolate",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Chocolate Bar"

def test_search_sweets_by_category(client, auth_token, db):
    """Test searching sweets by category"""
    sweet1 = Sweet(name="Chocolate Bar", category="Chocolate", price=Decimal("5.99"), quantity=10)
    sweet2 = Sweet(name="Gummy Bears", category="Candy", price=Decimal("3.99"), quantity=20)
    db.add_all([sweet1, sweet2])
    db.commit()
    
    response = client.get(
        "/api/sweets/search?category=Chocolate",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "Chocolate"

def test_search_sweets_by_price_range(client, auth_token, db):
    """Test searching sweets by price range"""
    sweet1 = Sweet(name="Expensive Sweet", category="Premium", price=Decimal("15.99"), quantity=10)
    sweet2 = Sweet(name="Cheap Sweet", category="Budget", price=Decimal("2.99"), quantity=20)
    db.add_all([sweet1, sweet2])
    db.commit()
    
    response = client.get(
        "/api/sweets/search?min_price=5.00&max_price=10.00",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 0  # Neither sweet is in the price range
    
    response = client.get(
        "/api/sweets/search?min_price=0.00&max_price=5.00",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Cheap Sweet"

def test_update_sweet_as_admin(client, admin_token, db):
    """Test updating a sweet as admin"""
    sweet = Sweet(name="Original", category="Test", price=Decimal("10.00"), quantity=20)
    db.add(sweet)
    db.commit()
    db.refresh(sweet)
    
    response = client.put(
        f"/api/sweets/{sweet.id}",
        json={
            "name": "Updated",
            "price": "12.99",
            "quantity": 25
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated"
    assert float(data["price"]) == 12.99
    assert data["quantity"] == 25

def test_delete_sweet_as_admin(client, admin_token, db):
    """Test deleting a sweet as admin"""
    sweet = Sweet(name="To Delete", category="Test", price=Decimal("10.00"), quantity=20)
    db.add(sweet)
    db.commit()
    db.refresh(sweet)
    sweet_id = sweet.id
    
    response = client.delete(
        f"/api/sweets/{sweet_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's deleted
    deleted_sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    assert deleted_sweet is None

def test_delete_sweet_as_user_unauthorized(client, auth_token, db):
    """Test that regular users cannot delete sweets"""
    sweet = Sweet(name="Protected", category="Test", price=Decimal("10.00"), quantity=20)
    db.add(sweet)
    db.commit()
    db.refresh(sweet)
    
    response = client.delete(
        f"/api/sweets/{sweet.id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_purchase_sweet(client, auth_token, db):
    """Test purchasing a sweet"""
    sweet = Sweet(name="Purchasable", category="Test", price=Decimal("10.00"), quantity=20)
    db.add(sweet)
    db.commit()
    db.refresh(sweet)
    
    response = client.post(
        f"/api/sweets/{sweet.id}/purchase",
        json={"quantity": 3},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["quantity"] == 17  # 20 - 3
    
    # Verify in database
    db.refresh(sweet)
    assert sweet.quantity == 17

def test_purchase_sweet_insufficient_quantity(client, auth_token, db):
    """Test purchasing more than available quantity"""
    sweet = Sweet(name="Limited", category="Test", price=Decimal("10.00"), quantity=2)
    db.add(sweet)
    db.commit()
    db.refresh(sweet)
    
    response = client.post(
        f"/api/sweets/{sweet.id}/purchase",
        json={"quantity": 5},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_purchase_sweet_zero_quantity(client, auth_token, db):
    """Test purchasing from a sweet with zero quantity"""
    sweet = Sweet(name="Out of Stock", category="Test", price=Decimal("10.00"), quantity=0)
    db.add(sweet)
    db.commit()
    db.refresh(sweet)
    
    response = client.post(
        f"/api/sweets/{sweet.id}/purchase",
        json={"quantity": 1},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_restock_sweet_as_admin(client, admin_token, db):
    """Test restocking a sweet as admin"""
    sweet = Sweet(name="Low Stock", category="Test", price=Decimal("10.00"), quantity=5)
    db.add(sweet)
    db.commit()
    db.refresh(sweet)
    
    response = client.post(
        f"/api/sweets/{sweet.id}/restock",
        json={"quantity": 20},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["quantity"] == 25  # 5 + 20
    
    # Verify in database
    db.refresh(sweet)
    assert sweet.quantity == 25

def test_restock_sweet_as_user_unauthorized(client, auth_token, db):
    """Test that regular users cannot restock"""
    sweet = Sweet(name="Stock", category="Test", price=Decimal("10.00"), quantity=10)
    db.add(sweet)
    db.commit()
    db.refresh(sweet)
    
    response = client.post(
        f"/api/sweets/{sweet.id}/restock",
        json={"quantity": 10},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN



from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from decimal import Decimal
from typing import List, Optional
from app.database import get_db
from app.models import Sweet, PurchaseHistory
from app.schemas import (
    SweetCreate, SweetUpdate, SweetResponse,
    PurchaseRequest, RestockRequest, PurchaseHistoryResponse, AdminPurchaseHistoryResponse
)
from app.dependencies import get_current_user, require_admin
from app.models import User

router = APIRouter()

@router.post("/", response_model=SweetResponse, status_code=status.HTTP_201_CREATED)
def create_sweet(
    sweet_data: SweetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    print(f"✅ create_sweet: User {current_user.username} (role: {current_user.role}) creating sweet: {sweet_data.name}", flush=True)
    sweet_dict = sweet_data.dict()
    sweet_dict['created_by_user_id'] = current_user.id  # Track which admin created this sweet
    db_sweet = Sweet(**sweet_dict)
    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)
    print(f"✅ Sweet created successfully: ID={db_sweet.id}", flush=True)
    return db_sweet

@router.get("/", response_model=List[SweetResponse])
def get_all_sweets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sweets = db.query(Sweet).all()
    return sweets

@router.get("/search", response_model=List[SweetResponse])
def search_sweets(
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Sweet)
    
    filters = []
    
    if name:
        filters.append(Sweet.name.ilike(f"%{name}%"))
    
    if category:
        filters.append(Sweet.category.ilike(f"%{category}%"))
    
    if min_price is not None:
        filters.append(Sweet.price >= Decimal(str(min_price)))
    
    if max_price is not None:
        filters.append(Sweet.price <= Decimal(str(max_price)))
    
    if filters:
        query = query.filter(and_(*filters))
    
    sweets = query.all()
    return sweets

# IMPORTANT: Sub-routes (purchase, restock) must come BEFORE the main {sweet_id} routes
# Otherwise FastAPI might match {sweet_id} to "purchase" or "restock"
@router.post("/{sweet_id}/purchase", response_model=SweetResponse)
def purchase_sweet(
    sweet_id: int,
    purchase_data: PurchaseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"🔍 purchase_sweet called: sweet_id={sweet_id}, quantity={purchase_data.quantity}", flush=True)
    db_sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    if db_sweet.quantity < purchase_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient quantity available"
        )
    
    if db_sweet.quantity == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sweet is out of stock"
        )
    
    db_sweet.quantity -= purchase_data.quantity
    
    # Save purchase history
    total_price = db_sweet.price * purchase_data.quantity
    purchase_record = PurchaseHistory(
        user_id=current_user.id,
        sweet_id=db_sweet.id,
        sweet_name=db_sweet.name,
        category=db_sweet.category,
        price=db_sweet.price,
        quantity=purchase_data.quantity,
        total_price=total_price
    )
    db.add(purchase_record)
    
    db.commit()
    db.refresh(db_sweet)
    print(f"✅ Purchase successful: {db_sweet.name} quantity now {db_sweet.quantity}", flush=True)
    return db_sweet

@router.post("/{sweet_id}/restock", response_model=SweetResponse)
def restock_sweet(
    sweet_id: int,
    restock_data: RestockRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    db_sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    db_sweet.quantity += restock_data.quantity
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

@router.put("/{sweet_id}/", response_model=SweetResponse)
def update_sweet(
    sweet_id: int,
    sweet_data: SweetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    db_sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    # Check if this sweet was created by a different admin
    if db_sweet.created_by_user_id and db_sweet.created_by_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit sweets that you created"
        )
    
    update_data = sweet_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(db_sweet, field, value)
    
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

@router.delete("/{sweet_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    db_sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    # Check if this sweet was created by a different admin
    if db_sweet.created_by_user_id and db_sweet.created_by_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete sweets that you created"
        )
    
    db.delete(db_sweet)
    db.commit()
    return None

@router.get("/purchase-history", response_model=List[PurchaseHistoryResponse])
def get_purchase_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get purchase history for the current user"""
    purchases = db.query(PurchaseHistory).filter(
        PurchaseHistory.user_id == current_user.id
    ).order_by(PurchaseHistory.purchased_at.desc()).all()
    return purchases

@router.get("/admin/purchase-history", response_model=List[AdminPurchaseHistoryResponse])
def get_all_purchase_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get purchase history for sweets created by this admin, purchased by regular users only"""
    from sqlalchemy.orm import joinedload
    
    # Get IDs of all sweets created by this admin
    admin_sweet_ids = db.query(Sweet.id).filter(
        Sweet.created_by_user_id == current_user.id
    ).subquery()
    
    # Only get purchases:
    # 1. Made by regular users (role='user')
    # 2. Of sweets created by this admin
    purchases = db.query(PurchaseHistory).join(User).filter(
        User.role == 'user',
        PurchaseHistory.sweet_id.in_(db.query(Sweet.id).filter(Sweet.created_by_user_id == current_user.id))
    ).order_by(PurchaseHistory.purchased_at.desc()).all()
    
    # Convert to AdminPurchaseHistoryResponse format
    result = []
    for purchase in purchases:
        user = db.query(User).filter(User.id == purchase.user_id).first()
        result.append({
            "id": purchase.id,
            "user_id": purchase.user_id,
            "username": user.username if user else "Unknown",
            "sweet_name": purchase.sweet_name,
            "category": purchase.category,
            "price": purchase.price,
            "quantity": purchase.quantity,
            "total_price": purchase.total_price,
            "purchased_at": purchase.purchased_at
        })
    return result


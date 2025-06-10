from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.models.item import Item
from app.models.user import User
from app.schemas.item import Item as ItemSchema, ItemCreate, ItemUpdate
from app.services.item_service import ItemService
from app.services.cache_service import CacheService
from app.services.notification_service import NotificationService
import json

router = APIRouter()
item_service = ItemService()
notification_service = NotificationService()
item_cache = CacheService("item", ItemSchema)

@router.get("/", response_model=List[ItemSchema])
async def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    search: str = Query(None, description="Search by title"),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve items.
    """
    if search:
        if current_user.is_superuser:
            items = item_service.search_by_title(db, title=search, skip=skip, limit=limit)
        else:
            # Filter by owner and search term
            items = (
                db.query(Item)
                .filter(Item.owner_id == current_user.id, Item.title.ilike(f"%{search}%"))
                .offset(skip)
                .limit(limit)
                .all()
            )
    else:
        if current_user.is_superuser:
            items = item_service.get_multi(db, skip=skip, limit=limit)
        else:
            items = item_service.get_multi_by_owner(
                db, owner_id=current_user.id, skip=skip, limit=limit
            )
    return items

@router.post("/", response_model=ItemSchema)
async def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: ItemCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new item.
    """
    item = item_service.create_with_owner(db, obj_in=item_in, owner_id=current_user.id)
    
    # Cache the item
    item_schema = ItemSchema.from_orm(item)
    await item_cache.set(f"{item.id}", item_schema)
    
    # Send notification
    notification_service.send_item_created_notification(
        current_user, item.title
    )
    
    return item

@router.get("/{id}", response_model=ItemSchema)
async def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get item by ID.
    """
    # Try cache first
    cached_item = await item_cache.get(f"{id}")
    if cached_item:
        if current_user.is_superuser or cached_item.owner_id == current_user.id:
            return cached_item
    
    # Get from database
    item = item_service.get(db, id=id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not enough permissions"
        )
    
    # Cache for future requests
    item_schema = ItemSchema.from_orm(item)
    await item_cache.set(f"{id}", item_schema)
    
    return item

@router.put("/{id}", response_model=ItemSchema)
async def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: ItemUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update an item.
    """
    item = item_service.get(db, id=id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not enough permissions"
        )
    
    item = item_service.update(db, db_obj=item, obj_in=item_in)
    
    # Update cache
    await item_cache.delete(f"{id}")
    
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> None:
    """
    Delete an item.
    """
    item = item_service.get(db, id=id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not enough permissions"
        )
    
    item_service.remove(db, id=id)
    
    # Remove from cache
    await item_cache.delete(f"{id}")

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from .base_service import BaseService


class ItemService(BaseService[Item, ItemCreate, ItemUpdate]):
    def __init__(self):
        super().__init__(Item)

    def create_with_owner(
        self, db: Session, *, obj_in: ItemCreate, owner_id: int
    ) -> Item:
        """
        Create a new item with owner
        """
        obj_in_data = obj_in.dict()
        db_obj = Item(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        """
        Get multiple items by owner
        """
        return (
            db.query(self.model)
            .filter(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
    def get_by_title(self, db: Session, *, title: str) -> Optional[Item]:
        """
        Get an item by title
        """
        return db.query(Item).filter(Item.title == title).first()
        
    def search_by_title(self, db: Session, *, title: str, skip: int = 0, limit: int = 100) -> List[Item]:
        """
        Search items by title
        """
        return (
            db.query(Item)
            .filter(Item.title.ilike(f"%{title}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

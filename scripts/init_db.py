#!/usr/bin/env python3
"""
Initialize database with sample data
"""
import asyncio
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.user import User
from app.models.item import Item
from app.core.database import Base
from app.services.user_service import UserService
from app.services.item_service import ItemService
from app.schemas.user import UserCreate
from app.schemas.item import ItemCreate

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    user_service = UserService()
    item_service = ItemService()
    
    # Create superuser
    superuser = user_service.get_by_email(db, email="admin@example.com")
    if not superuser:
        superuser_in = UserCreate(
            email="admin@example.com",
            username="admin",
            full_name="Administrator",
            password="admin123",
            is_superuser=True,
        )
        superuser = user_service.create(db, obj_in=superuser_in)
        print("✅ Superuser created")
    
    # Create sample user
    user = user_service.get_by_email(db, email="user@example.com")
    if not user:
        user_in = UserCreate(
            email="user@example.com",
            username="user",
            full_name="Regular User",
            password="user123",
        )
        user = user_service.create(db, obj_in=user_in)
        print("✅ Sample user created")
    
    # Create sample items
    if db.query(Item).count() == 0:
        items = [
            ItemCreate(title="Sample Item 1", description="This is a sample item"),
            ItemCreate(title="Sample Item 2", description="Another sample item"),
            ItemCreate(title="Admin Item", description="Admin's item"),
        ]
        
        item_service.create_with_owner(db, obj_in=items[0], owner_id=user.id)
        item_service.create_with_owner(db, obj_in=items[1], owner_id=user.id)
        item_service.create_with_owner(db, obj_in=items[2], owner_id=superuser.id)
        
        print("✅ Sample items created")
    
    db.close()
    print("🎉 Database initialization completed!")

if __name__ == "__main__":
    init_db()

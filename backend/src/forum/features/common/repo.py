
from abc import ABC
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from forum.features.common.entities import BaseEntity, OwnableEntity, ViewableEntity
from forum.features.query import PaginationQuery
from forum.features.user.database.models import User
from sqlalchemy import update
from sqlalchemy.orm import Session

T = TypeVar("T", bound=BaseEntity)

class BaseRepo(ABC, Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
        
class CRUDRepo(BaseRepo[T]):
        
    def create(self, entity: T) -> T:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        entity = self.db.query(self.model).filter(self.model.id == entity_id).first()
        return entity
    
    def get_all(self, pagination: Optional[PaginationQuery] = None) -> List[T]:
        query = self.db.query(self.model)
        if pagination:
            query = query.limit(pagination.limit).offset(pagination.offset)
            
        return query.all()
    
    def update(self, entity_id: int, **kwargs: Any) -> Optional[T]:
        entity = self.get_by_id(entity_id)
        if not entity:
            return None
        for key, value in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        self.db.flush()
        self.db.refresh(entity)
        return entity
    
    def delete(self, entity_id: int) -> bool:
        entity = self.get_by_id(entity_id)
        if not entity:
            return False
        self.db.delete(entity)
        self.db.flush()
        return True

V = TypeVar("V", bound=ViewableEntity)

class ViewableRepo(BaseRepo[V]):
    def increment_views(self, entity_id: int) -> Optional[int]:
        stmt = (
            update(self.model)
            .where(self.model.id == entity_id)
            .values(view_count=self.model.view_count + 1)
            .returning(self.model.view_count)
        )
        result = self.db.execute(stmt)
        self.db.flush() 
        return result.scalar_one_or_none()
    
U = TypeVar("U", bound=OwnableEntity)
class OwnableRepo(BaseRepo[U]):
    def get_owner(self, entity_id: int) -> Optional[User]:
        entity = self.db.query(self.model).filter(self.model.id == entity_id).first()
        if entity:
            return entity.creator
        return None
    
    def get_all_by_owner(self, owner_id: int, pagination: Optional[PaginationQuery] = None) -> List[U]:
        query = self.db.query(self.model).where(self.model.creator_id == owner_id)
        if pagination:
            query = query.limit(pagination.limit).offset(pagination.offset)
            
        return query.all()
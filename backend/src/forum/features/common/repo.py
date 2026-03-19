
from abc import ABC
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from forum.features.common.mixins import IdMixin
from forum.features.query import PaginationQuery
from sqlalchemy.orm import DeclarativeBase, Session

T = TypeVar("T", bound=IdMixin)


class BaseRepo(ABC, Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
        
class CRUDRepo(BaseRepo[T]):
    def __init__(self, db: Session, model: Type[T]):
        super().__init__(db, model)
        
    def create(self, entity: T) -> T:
        self.db.add(entity)
        self.db.commit()
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
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def delete(self, entity_id: int) -> bool:
        entity = self.get_by_id(entity_id)
        if not entity:
            return False
        self.db.delete(entity)
        self.db.commit()
        return True
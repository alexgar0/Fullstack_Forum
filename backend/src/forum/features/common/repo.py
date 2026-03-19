from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, List, Optional, Sequence, Type, TypeVar
from forum.features.common.entities import BaseEntity, OwnableEntity, ViewableEntity
from forum.features.common.schemas import PaginationDTO
from forum.features.query import PaginationQuery
from forum.features.user.database.models import User
from pydantic import BaseModel
from sqlalchemy import ColumnExpressionArgument, func, select, update
from sqlalchemy.orm import Session

X = TypeVar("X")

@dataclass
class PaginationResult(Generic[X]):
    items: Sequence[X]
    current_offset: int
    total_items: int
    limit: int
    
    def to_dto(self) -> PaginationDTO:
        return PaginationDTO(current_offset=self.current_offset, total_items=self.total_items, limit=self.limit)
    
    
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

    def get_page(
        self, 
        *filters: ColumnExpressionArgument[bool],
        pagination: Optional[PaginationQuery] = None
    ) -> PaginationResult[T]:
        
        base_stmt = select(self.model)
        if filters:
            base_stmt = base_stmt.where(*filters)
            
        data_stmt = base_stmt
        current_offset = 0
        
        if pagination:
            current_offset = pagination.offset
            data_stmt = data_stmt.limit(pagination.limit).offset(pagination.offset)
        
        items = self.db.execute(data_stmt).scalars().all()
        
        count_stmt = select(func.count()).select_from(base_stmt.alias()) 
        total_items = self.db.scalar(count_stmt) or 0
        
        return PaginationResult(items=items, total_items=total_items, current_offset=current_offset, limit=pagination.limit if pagination else 0)

    def get_all(self, *filters: ColumnExpressionArgument[bool]) -> Sequence[T]:
        stmt = select(self.model)
        if filters:
            stmt = stmt.where(*filters)
        
        result = self.db.execute(stmt)
        return result.scalars().all()

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

    def get_all_by_owner(
        self, owner_id: int, pagination: Optional[PaginationQuery] = None
    ) -> List[U]:
        query = self.db.query(self.model).where(self.model.creator_id == owner_id)
        if pagination:
            query = query.limit(pagination.limit).offset(pagination.offset)

        return query.all()
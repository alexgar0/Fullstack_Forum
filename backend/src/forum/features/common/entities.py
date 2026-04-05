from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Self

from forum.features.common.mixins import (
    CreatedAtMixin,
    EditableMixin,
    IdMixin,
    ViewsMixin,
    OwnableByUserMixin,
)

if TYPE_CHECKING:
    from forum.features.common.repo import CRUDRepo


class BaseEntity(IdMixin):
    pass


class ViewableEntity(BaseEntity, ViewsMixin):
    pass


class OwnableEntity(BaseEntity, OwnableByUserMixin):
    pass


class CreatedAtEntity(BaseEntity, CreatedAtMixin):
    pass


class EditableEntity(CreatedAtEntity, EditableMixin):
    def edited(self, repo: "CRUDRepo[Self]") -> None:
        repo.update(self.id, last_edited_at=datetime.now())
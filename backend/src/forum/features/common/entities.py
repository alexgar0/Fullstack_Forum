from forum.features.common.mixins import (
    CreatedAtMixin,
    EditableMixin,
    IdMixin,
    ViewsMixin,
    OwnableByUserMixin,
)


class BaseEntity(IdMixin):
    pass


class ViewableEntity(BaseEntity, ViewsMixin):
    pass


class OwnableEntity(BaseEntity, OwnableByUserMixin):
    pass


class CreatedAtEntity(BaseEntity, CreatedAtMixin):
    pass


class EditableEntity(CreatedAtEntity, EditableMixin):
    pass

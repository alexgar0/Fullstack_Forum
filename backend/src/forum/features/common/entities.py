from forum.features.common.mixins import IdMixin, ViewsMixin, OwnableByUserMixin

class BaseEntity(IdMixin):
    pass

class ViewableEntity(BaseEntity, ViewsMixin):
    pass

class OwnableEntity(BaseEntity, OwnableByUserMixin):
    pass
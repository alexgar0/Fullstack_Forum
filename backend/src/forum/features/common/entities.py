from forum.features.common.mixins import IdMixin, ViewsMixin

class BaseEntity(IdMixin):
    pass

class ViewableEntity(BaseEntity, ViewsMixin):
    pass
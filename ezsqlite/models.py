from . import expections
from . import util


class Model(object):
    def __init__(self, **kwargs):
        pk_num = 0
        for k, w in kwargs.items():
            field = getattr(self.__class__, k)
            if field.PRIMARY_KEY:
                pk_num += 1
            if pk_num > 1:
                raise expections.FieldException('Too many PRIMARY KEY.')
            if field.NOT_NULL and w is None:
                raise expections.FieldException(k + ' must not be None.')
            setattr(self, k, w)

    def __repr__(self):
        return vars(self).__repr__()

    @classmethod
    def create(cls):
        q = util._Query(cls)
        q._create()
        q.exec()

    @classmethod
    def drop(cls):
        q = util._Query(cls)
        q._drop()
        q.exec()

    @classmethod
    def all(cls):
        q = util._Query(cls)
        q._select_all()
        return q

    @classmethod
    def count(cls):
        q = util._Query(cls)
        q._count()
        return q

    @classmethod
    def distinct(cls):
        q = util._Query(cls)
        q._distinct()
        return q

    @classmethod
    def search(cls, condition=None, **kwargs):
        q = util._Query(cls)
        q._select_all()
        q.where(condition, **kwargs)
        return q

    @classmethod
    def update(cls, **kwargs):
        q = util._Query(cls)
        q._update(**kwargs)
        return q

    @classmethod
    def remove(cls):
        q = util._Query(cls)
        q._delete()
        return q

    def save(self):
        q = util._Query(self.__class__)
        q._insert(self)
        q.exec()


class _Field(object):
    def __init__(self,
                 default=None,
                 PRIMARY_KEY=False,
                 NOT_NULL=False,
                 AUTOINCREMENT=False):

        self.__PRIMARY_KEY = PRIMARY_KEY
        self.__NOT_NULL = NOT_NULL or PRIMARY_KEY
        self.__default = default
        self.__AUTOINCREMENT = AUTOINCREMENT

    @property
    def PRIMARY_KEY(self):
        return self.__PRIMARY_KEY

    @property
    def NOT_NULL(self):
        return self.__NOT_NULL

    @property
    def default(self):
        return self.__default

    @property
    def AUTOINCREMENT(self):
        return self.__AUTOINCREMENT


class TextField(_Field):
    pass


class NumericField(_Field):
    pass


class IntField(_Field):
    pass


class RealField(_Field):
    pass


class NoneField(_Field):
    pass

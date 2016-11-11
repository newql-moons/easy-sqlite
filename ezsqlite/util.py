from . import models
from . import db


class _Query(object):
    def __init__(self, model):
        self.__tab = model
        self.__script = ''
        self.__params = []

    @property
    def script(self):
        script = self.__script.replace('?', '%s') % tuple(self.__params)
        return script + ';'

    def _create(self):
        sql = 'CREATE TABLE %s ( ' % self.__tab.Meta.name
        for k, w in vars(self.__tab).items():
            if isinstance(w, models._Field):
                sql += k
                sql += ' %s'
                if w.PRIMARY_KEY:
                    sql += ' PRIMARY KEY'
                if w.NOT_NULL and not w.PRIMARY_KEY:
                    sql += ' NOT NULL'
                if w.default:
                    sql += (' DEFAULT \'' + str(w.default) + '\'')
                sql += ', '
            if isinstance(w, models.IntField):
                sql %= 'INT'
            if isinstance(w, models.RealField):
                sql %= 'REAL'
            if isinstance(w, models.NoneField):
                sql %= 'NONE'
            if isinstance(w, models.NumericField):
                sql %= 'NUMERIC'
            if isinstance(w, models.TextField):
                sql %= 'TEXT'
        self.__script = (sql[:len(sql) - 2] + ' )')

    def _insert(self, item):
        sql = 'INSERT INTO %s ( ' % self.__tab.Meta.name
        st = ' VALUES ('
        for k, w in vars(item).items():
            sql += k
            sql += ', '
            st += '?, '
        sql = sql[:len(sql) - 2] + ' )'
        st = st[:len(st) - 2] + ')'
        sql += st
        self.__params.extend([w for k, w in vars(item).items()])
        self.__script = sql

    def _select_all(self):
        self.__script = ('SELECT * FROM %s' % self.__tab.Meta.name)

    def _update(self, **kwargs):
        self.__script = 'UPDATE %s SET ' % self.__tab.Meta.name
        tmp = ''
        for k, w in kwargs.items():
            tmp += ('%s = ?, ' % k)
            self.__params.append(w)
        tmp = tmp[:len(tmp) - 2]
        self.__script += tmp

    def _delete(self):
        self.__script = 'DELETE FROM %s' % self.__tab.Meta.name

    def _condition(self, condition, **kwargs):
        if isinstance(condition, str):
            self.__script += condition
        else:
            for k, w in kwargs.items():
                self.__params.append(w)
                self.__script += ('%s = ?' % k)

    def where(self, condition=None, **kwargs):
        self.__script += ' WHERE '
        self._condition(condition, **kwargs)
        return self

    def Or(self, condition=None, **kwargs):
        self.__script += ' OR '
        self._condition(condition, **kwargs)
        return self

    def And(self, condition=None, **kwargs):
        self.__script += ' AND '
        self._condition(condition, **kwargs)
        return self

    def limit(self, num):
        self.__script += (' LIMIT %s' % num)
        return self

    def __iter__(self):
        if len(self.__params):
            cs = db._instance(self.__tab.Meta.database).execute(self.__script, self.__params)
        else:
            cs = db._instance(self.__tab.Meta.database).execute(self.__script)
        for row in cs:
            yield self.__tab(**row)

    def exec(self):
        if len(self.__params):
            db._instance(self.__tab.Meta.database).execute(self.__script, self.__params)
        else:
            db._instance(self.__tab.Meta.database).execute(self.__script)
        db._instance(self.__tab.Meta.database).commit()

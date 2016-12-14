from . import models
from . import db


class _Query(object):
    def __init__(self, model):
        self.__tab = model
        self.__script = ''
        self.__params = []
        
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

    def items(self):
        return list(self)

    def item(self):
        try:
            return list(self)[0]
        except:
            return None

    @property
    def count(self):
        script = self.__script.replace('SELECT *', 'SELECT COUNT(*)')
        if len(self.__params):
            cs = db._instance(self.__tab.Meta.database).execute(script, self.__params)
        else:
            cs = db._instance(self.__tab.Meta.database).execute(script)
        return cs.fetchone()[0]

    @property
    def script(self):
        if len(self.__params):
            script = self.__script.replace('?', '%s') % tuple(self.__params)
        else:
            script = self.__script
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
                if w.AUTOINCREMENT:
                    sql += ' AUTOINCREMENT'
                sql += ', '
            if isinstance(w, models.IntField):
                sql %= 'INTEGER'
            if isinstance(w, models.RealField):
                sql %= 'REAL'
            if isinstance(w, models.NoneField):
                sql %= 'NONE'
            if isinstance(w, models.NumericField):
                sql %= 'NUMERIC'
            if isinstance(w, models.TextField):
                sql %= 'TEXT'
        self.__script = (sql[:len(sql) - 2] + ' )')

    def _drop(self):
        self.__script = 'DROP TABLE %s' % self.__tab.Meta.name

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

    def _distinct(self):
        self.__script = ('SELECT DISTINCT * FROM %s' % self.__tab.Meta.name)

    def _count(self):
        self.__script = ('SELECT COUNT(*) FROM %s' % self.__tab.Meta.name)

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
            if len(kwargs) > 1:
                tmp = ''
                for k, w in kwargs.items():
                    self.__params.append(w)
                    tmp += (' AND %s = ?' % k)
                self.__script += tmp[4:]
            else:
                k, w = list(kwargs.items())[0]
                self.__params.append(w)
                self.__script += ('%s = ?' % k)

    def where(self, condition=None, **kwargs):
        self.__script += ' WHERE '
        self._condition(condition, **kwargs)
        return self

    def having(self, condition=None, **kwargs):
        self.__script += ' HAVING '
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

    def offset(self, index):
        self.__script += (' OFFSET %s' % index)
        return self

    def order_by(self, *args):
        tmp = ' ORDER BY'

        for column in args:
            tmp += (' %s,' % column)
        self.__script += tmp[:len(tmp) - 1]
        return self

    def group_by(self, *args):
        tmp = ' GROUP BY'

        for column in args:
            tmp += (' %s,' % column)
        self.__script += tmp[:len(tmp) - 1]
        return self

    @property
    def ASC(self):
        self.__script += ' ASC'
        return self

    @property
    def DESC(self):
        self.__script += ' DESC'
        return self

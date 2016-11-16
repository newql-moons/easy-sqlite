#Easy SQLite

这个库可以用于便捷的操作SQLite数据库。使用这个库可以使您的程序使用简洁的Python脚本代替冗长SQL语句来查询或更新多个项目中的多个数据库。

###开始

首先您您需要创建**Model**来对应您的每一个数据表。

>示例

假如您有这样一张表在您的数据库中

**tables.sql**
```SQL
CREATE TABLE student (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  age INTEGER 
);
```

您可以这样编写**Model**来对应它。

**tables.py**

```python
from ezsqlite import models

DB_PATH = 'db.sqlite3' #您的SQLite目录，可任意选取

class Student(models.Model):
    id = models.IntField(PRIMARY_KEY=True)
    name = models.TextField(NOT_NULL=True)
    age = models.IntField()
    class Meta:
        name = 'student' # 指定表名(必须和数据库中的表名一致)
        database = DB_PATH
```

这样就已经可以在您的项目中对这个数据表进行操作了。

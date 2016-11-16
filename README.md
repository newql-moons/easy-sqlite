#Easy SQLite

这个库可以用于便捷的操作SQLite数据库。使用这个库可以使您的程序使用简洁的Python脚本代替冗长SQL语句来查询或更新多个项目中的多个数据库。

###开始

首先您您需要创建**Model**来对应您的每一个数据表。

>示例

**tables.sql**
```SQL
CREATE TABLE student (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  age INTEGER 
);
```

**tables.py**
```python
from ezsqlite import models

DB_PATH = 'db.sqlite3'

class Student(models.Model):
    id = models.IntField(PRIMARY_KEY=True)
    name = models.TextField(NOT_NULL=True)
    age = models.IntField()
    class Meta:
        name = 'student'
        database = DB_PATH
```

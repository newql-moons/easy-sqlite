# Easy SQLite

这个库可以用于便捷的操作SQLite数据库。使用这个库可以使您的程序使用简洁的Python脚本代替冗长的SQL语句来查询或更新多个数据库中的多个表格。

### 开始

首先您您需要创建`Model`来对应您的每一个数据表。

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

您可以这样编写`Model`来对应它。

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

### 连接数据库

在使用这些`Model`前您还需要连接数据库

>连接单一数据库

```python
from ezsqlite import db

DB_PATH = 'db.sqlite3'

db.connect(DB_PATH)
```

>连接多个数据库

```python
from ezsqlite import db

DB_PATH = [
    'db1.sqlite3',
    'db2.sqlite3',
]

db.connect(DB_PATH)
```

在完成所有数据库操作之后，您需要断开这些数据库连接

```python
from ezsqlite import db

db.disconnect()
```
这样就已经可以在您的项目中对这个数据表进行操作了。

### 向表格插入数据

>示例

我们向之前创建的表格`student`中插入一行数据

```Python
Student(id=1, name='李华', age=20).save()
```

这时候查询student表格

|id|name|age|
|:---:|:---:|:---:|
|1|李华|20|

 类似地，再向`student`中插入两行数据

```Python
Student(id=2, name='月梦书', age=20).save()
Student(id=3, name='小明', age=18).save()
```

再次查询`student`

|*id*|*name*|*age*|
|:---:|:---:|:---:|
|1|李华|20|
|2|月梦书|20|
|3|小明|18|

### 查询

>查询所有

我们先查询`student`中的所有数据并打印在终端上

```python
for item in Stuent.all():
    print(item)
```

**终端**

    {'age': 20, 'id': 1, 'name': '李华'}
    {'age': 20, 'id': 2, 'name': '月梦书'}
    {'age': 18, 'id': 3, 'name': '小明'}

也可以这样来访问`student`的每个字段

```Python
    for item in Student.all():
        print('id: %s, name: %s, age: %s' % (item.id, item.name, item.age))
```

**终端**

    id: 1, name: 李华, age: 20
    id: 2, name: 月梦书, age: 20
    id: 3, name: 小明, age: 18

`Student.all()`会返回一个迭代对象，如果您需要一个查询结果的`list`,您可以这样

```Python
students = list(Student.all())
```

>条件查询

查询`age=20`的所有`student`
```Python
for item in Student.search(age=20):
    print(item)
```

**终端**

    {'age': 20, 'id': 1, 'name': '李华'}
    {'age': 20, 'id': 2, 'name': '月梦书'}

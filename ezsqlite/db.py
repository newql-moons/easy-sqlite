import sqlite3


_conn = {}


def connect(arg):
    global _conn
    if isinstance(arg, str):
        _conn[arg] = sqlite3.connect(arg)
        _conn[arg].row_factory = sqlite3.Row
    elif isinstance(arg, list):
        for item in arg:
            _conn[item] = sqlite3.connect(item)
            _conn[item].row_factory = sqlite3.Row
    else:
        raise TypeError()


def _instance(database):
    global _conn
    return _conn[database]


def disconnect():
    for k, w in _conn.items():
        w.close()

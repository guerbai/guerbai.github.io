---
title: records库源码阅读
date: 2019-01-30 19:14:12
tags:
- 源码阅读
- python
---

翻requests作者kennethreitz的repositories时发现了该库，想起之前做报表用index对应key的痛苦经历。
原来这样的问题早已被解决掉了。

k神300多行代码便得了3000多个star。

<!--more-->

该项目本质上依然是对sqlalchemy的包装。

# 创建cli应用

该库包提供了一个命令行服务，直接在终端输入records即可运行，代码中最后一个函数cli()实现了这一点。

稍微探究了一下实现到命令行的过程：

既然是可在命令行中被运行，必然在某个/bin文件夹下有其运行文件，binary or soft link。
```shell
$ ll /usr/bin | grep records
```

在/usr/bin文件夹下找到了records文件。
至于soft link的情况，会出现`records -> **`的情况。而上述命令的结果只有`records`，看来不是soft link。

```python
$ cat /usr/bin/records
```

该命令输入了一段python脚本，引入了records.cli。处理了args后，运行`sys.exit(cli())`。
`records <args>`输入的命令行参数会被cli函数使用到，而cli的返回值便作为脚本退出的返回码。

也就是pip下载该库时其放了一个python文件到了/usr/bin/records。

# 元组到字典，半orm

其对sqlalchemy进行了包装，在sqlalchemy中使用execute sql返回的结果为元组，要做api的话，还要根据index一个一个去构造字典，而k神用了一些处理便解决了这个问题。

其Record类实例化时接受两个元组参数，keys与value。前者为select 之后的key，而value为返回结果，将两者一一对应起来，形成字典的形式。

```Python

    def __getitem__(self, key):
        # Support for index-based lookup.
        if isinstance(key, int):
            return self.values()[key]

        # Support for string-based lookup.
        if key in self.keys():
            i = self.keys().index(key)
            return self.values()[i]

    def as_dict(self, ordered=False):
        """Returns the row as a dictionary, as ordered."""
        items = zip(self.keys(), self.values())

        return OrderedDict(items) if ordered else dict(items)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(e)

    def get(self, key, default=None):
        """Returns the value for a given key, or default."""
        try:
            return self[key]
        except KeyError:
            return default
```

说一下实现，`__getitem__`是像字典一样取值时会被调用，如`record=Record(keys, values); record['a']`这样。
可以看到，其不但支持以key为key，亦支持以index为key，仍然保留了sqlalchemy其自身行为的兼容性，使用起来真的是方便。

而之前的一一对应化为字典的活只用一个zip便轻松解决。
该函数举例如下：
```Python
>>> a = ['a', 'b', 'c'];b = [1, 2, 3]; c = dict(zip(a, b))
>>> c
{'a': 1, 'c': 3, 'b': 2}
```

在`__getattr__`中实现了点操作符取值。get方法则对应到字典的.get()功能。

# RecordCollection

RecordCollection中实现了迭代器的魔法方法`__iter__`与`__next__`。
使用一个bool字段pending来表示迭代是否完成。
使用这种实现亦考虑了内存占用，性能等问题。

在Database类中，一个query语句之后，将sqlalchemy的结果构造为一个generator，传入RecordCollection类。
```Python
# Execute the given query.
cursor = self.db.execute(text(query), **params) # TODO: PARAMS GO HERE

# Row-by-row Record generator.
row_gen = (Record(cursor.keys(), row) for row in cursor)

# Convert psycopg2 results to RecordCollection.
results = RecordCollection(row_gen)
```

在该类中，将对该类的迭代映射到自身的_rows字段上，并将已迭代出来的结果放入_all_rows字段。
这段实现很精彩，代码如下：
```Python
class RecordCollection(object):
    """A set of excellent Records from a query."""
    def __init__(self, rows):
        self._rows = rows
        self._all_rows = []
        self.pending = True

    def __repr__(self):
        return '<RecordCollection size={} pending={}>'.format(len(self), self.pending)

    def __iter__(self):
        """Iterate over all rows, consuming the underlying generator
        only when necessary."""
        i = 0
        while True:
            # Other code may have iterated between yields,
            # so always check the cache.
            if i < len(self):
                yield self[i]
            else:
                # Throws StopIteration when done.
                # Prevent StopIteration bubbling from generator, following https://www.python.org/dev/peps/pep-0479/
                try:
                    yield next(self)
                except StopIteration:
                    return
            i += 1

    def next(self):
        return self.__next__()

    def __next__(self):
        try:
            nextrow = next(self._rows)
            self._all_rows.append(nextrow)
            return nextrow
        except StopIteration:
            self.pending = False
            raise StopIteration('RecordCollection contains no more rows.')

    def __getitem__(self, key):
        is_int = isinstance(key, int)

        # Convert RecordCollection[1] into slice.
        if is_int:
            key = slice(key, key + 1)

        while len(self) < key.stop or key.stop is None:
            try:
                next(self)
            except StopIteration:
                break

        rows = self._all_rows[key]
        if is_int:
            return rows[0]
        else:
            return RecordCollection(iter(rows))

    def __len__(self):
        return len(self._all_rows)

    def export(self, format, **kwargs):
        """Export the RecordCollection to a given format (courtesy of Tablib)."""
        return self.dataset.export(format, **kwargs)

    def all(self, as_dict=False, as_ordereddict=False):
        """Returns a list of all rows for the RecordCollection. If they haven't
        been fetched yet, consume the iterator and cache the results."""

        # By calling list it calls the __iter__ method
        rows = list(self)

        if as_dict:
            return [r.as_dict() for r in rows]
        elif as_ordereddict:
            return [r.as_dict(ordered=True) for r in rows]

        return rows
```

# Database类

在主类中，实现了上下文管理的with方法相关的魔法方法。在进入和退出时处理连接的开启与关闭，十分优雅。让使用者无需关心这些事情。
```Python
    def close(self):
        """Closes the connection to the Database."""
        self.db.close()
        self.open = False

    def __enter__(self):
        return self

    def __exit__(self, exc, val, traceback):
        self.close()
```

# 各种格式的导出

该库还提供了各种格式如json，xls，cvs的导出功能，是结合tablib库实现的。
[tablib文档](http://docs.python-tablib.org/en/latest/)
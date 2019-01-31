---
title: june源码阅读
date: 2017-07-10 16:10:32
tags:
- python
- 源码阅读
---

之前在知乎上关于开源项目的答案中看到某答出提到了[该项目](https://github.com/lepture/june)，以及其中的一些精巧的实现。

项目代码量并不大，然由于年代久远，各种库的版本变化大太，API有一些出入，已很难将项目跑起来。
我在阅读源码的过程中学到了一些东西，记录在此。

<!--more-->

# werkzeug.cached_property

做一个对象属性的缓存。

```Python
from werkzeug import cached_property

class Foo(object):

    @cached_property
    def foo(self):
        print 'in foo'
        # some cost time thing.
        return 'ok'

bar = Foo()
print bar.foo
print bar.foo
```
输入结果为：
```
in foo
ok
ok
```
可以得到两点结论：
1. 经cached_property装饰后，foo成为了Foo()的一个属性而不再是函数。
2. 仅在第一次被调用时会运行foo函数，之后的结果被缓存了起来，再次调foo属性，不会运行foo()函数。

# 自定义基础查询类

在models/_base.py中，实现了一个JuneQuery类，继承了BaseQuery。增加了两个方法。

可以看到flask-sqlalchemy库中Model类有一个query_class属性，默认便指向BaseQuery。
而在db声明中，使用`query_class=JuneQuery`，便可以做到了对此类进行查询时，使用JuneQuery而不是BaseQuery。


这可以解决一个场景，比如可以重写get_or_404()方法，认为找不到记录是出了错误，要报警，便可由此法解决。

此处是一个切入口。
亦可重写query，filter_by, filter，all等方法，或增加其他方法给Model实例使用。

# 类`__call__`方法作为装饰器

当python的类实现了__call__方法时，其实例可像函数一样被调用。
如：
```Python
class A(object):
    def __call__(self, args):
        print 'called with args: ' + args
        return 'ok'

a = A()
a('are you ')
```

项目中helpers.py中实现了两个这样的类，require_role与limit_request。
关注点在于，这两个类将__call__实现为了一个装饰器。
```Python
class require_role(object):
    def __init__(self, role):
        self.role = role

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            if g.user.role == 'admin':
                return method(*args, **kwargs)
            if g.user.role != self.role:
                return abort(403)
            # other situation long code.
            return method(*args, **kwargs)
        return wrapper
```

这样，由于类在实例化时，便可以传入参数，同时实例化之后，亦可以调用其他方法，做一些改变。
此时，这个实例，又可以作为一个装饰器，由此便获得了极大的灵活性。

这与三层装饰器不同。
三层装饰器，在最外一层可以写一些代码逻辑，然而与这种方法相比，三层装饰器的最外层便相当于硬编码。
该方法操作一个类实例，可以根据不同情况被调用各种方法进行属性操作等，之后再作为装饰器使用，它的**装饰效果是动态的**。

# permanent实现

登陆使用的是flask的session功能，session具有一个permanent属性，可将其设为True。
对于session的生命周期与使用，我写一个test，做了一些尝试。

```Python
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'fyb'

count = 1

@app.route("/")
def index():
    global count
    session['id'] = count
    count += 1
    return 'hello'

@app.route("/test")
def test():
    print session
    return 'session'

if __name__ == '__main__':
    app.run()
```
当使用curl来测试，先调'/'路由，再调'/test'路由，打印的session结果为：
> SecureCookieSession {}

而使用浏览器打开，同样的操作顺序，结果为：
> SecureCookieSession {u'id': 2}

可见，flask的session是浏览器相关的，并不会搞混掉。curl的操作中并没有提供像浏览器一样的上下文环境。
需要注意的是，要使用session功能，需要app的secret_key。
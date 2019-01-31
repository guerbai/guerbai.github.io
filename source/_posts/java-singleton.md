---
title: 关于Java单例模式需要知道的
date: 2018.10.23 10:19:00
tags:
- java
- 读书
- 源码阅读
---

单例模式，甚至是所有的二十几种设计模式，已经是一个被说得快要烂掉的话题了。  
笔者也自觉网上太多类似内容未免有些聒噪，然而最近在看《[Java编程思想](https://book.douban.com/subject/2130190/)》时，意识到该书之意味无穷有很大一部分原因在于将各色设计模式整合于各处，在描述讲解Java语言的设计时，各种成熟的设计便在例子与解读中缓缓流淌而出。  

诚然，要论设计模式，若用Python来举例，总不免会感觉一些例子着实有些迁强，而Java才是设计模式生长的沃土，在很多内置库中便采用了这些设计与实现。  

<!--more-->

故笔者意欲总结、学习一下在该书、Java内置语言实现方面所用到的设计模式，以及采用这种设计的思考，并不同于网上随处可见模式讲解以及代码罗列。  
遂有些篇。


# Singleton in `<Thinking in Java>`

作者在第六章 *访问控制权限* 的 *类的访问权限* 中即举了一个 *单例模式* 的例子，此时前面的章节只讲了操作符、 `if-else` 与构造器的内容，连函数都没开讲，甚至在代码例子中设计到 `public static Soup1 makeSoup()` 这样的语句也要跟读者补充一下Soup1是返回值的类型的知识。  
那作者何故要在此节的例子中直接引入设计模式这样相对而言更为高深的话题呢？这对于作者讲解类的访问权限有什么帮助呢？

例子很简单，诸君想必已见过无数次：

```java
class Soup {
    private Soup() {}

    private static Soup ps1 = new Soup();

    public static Soup access() {
        return ps1;
    }

}
```

一个常见的单例写法，看到代码之后很容易明悉作者的意图，正是由于该类的构造函数被设定为private，才保证其不能被客户端任意实例化，只能通过类设计者提供的唯一入口来获取此实例，保证了单例的唯一性。  

此时反观Python，由于其并未具有类似Java语言private提供的这种保证，其单例模式的实现看起来更像是一种hack，需要对Python有一些更深入的理解才可领悟，对比如下：

```python
class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance

```

显然，就两种版本而言，Python的实现相较于Java需要对语言本身更为深入的理解。  
要看懂Python版本的单例模式，你需要了解到Python `__init__` 与 `__new__` 的区别， `*args` 与 `**kw` 这种写法的意思以及继承的有关知识。  

本书后文 *类型信息* 一章 *空对象* 一节，给出了一个使用单例模式的典型场景。  
使用一个static final的单例来表示系统中的空对象，比如一个不存在的Person，可以保证该对象不被改变，从而给系统带来一个有效的对象，并且可以减少和优化四处判断空指针的dirty code。


# 几种写法的考量

在单例模式的实现上也有一定的差异，这其中设计到一些效率与线程安全性方面的考量，并不是“茴香豆”的茴有几种写法一般的炫技取乐。


## 延迟加载

在上面关于Soup的例子中，可以看出在类被加载时其单例便已经被构造成功了。  
这就好比饭店煮了一碗汤，材料与能源直接消耗掉，却不一定有顾客去真的喝这碗汤，这便形成了一种浪费。  
在大型程序中，有些对象的构造的确是要消耗比较大的资源的，等到有顾客需要时，才去构造，会是一种行之有效的优化。  

```java
class Soup {
    private Soup() {}

    private static Soup ps1;

    public static Soup access() {
        if (ps1 == null) {
            ps1 = new Soup();
        }
        return ps1;
    }

}
```

如此便是一种优化了。


## 线程安全性

然而，上面的例子是有隐患的，它并不是线程安全的，由于存在[竞态条件](https://github.com/guerbai/it-does-works)的问题，以上的写法在多线程环境下，只是 **有可能** 运行正确，实际上它无法保证该类只有一个实例。  
其实要消除这种隐患很简单，将access方法标记为synchronized即可。  

```java
public static synchronized Soup access() {
    if (ps1 == null) {
        ps1 = new Soup();
    }
    return ps1;
}
```

然而，对线程安全性的保证往往是有性能代价的，上述写法的synchronized实际上只是为了保护ps1的确为null时的情况，而当其已被实例化之后多个线程再去access时，也会受到一定的性能影响，而此时synchronized其实是不再需要了的。  

为解决此问题，又有一些其他的写法，比如 *内部类* 、 *双重检查* 、 *enum* 等，具体代码就不帖了，网上四处皆是。  
这些实现引入了额外的代码复杂度以及Java语言的细节，我以为有些得不偿失。  
因为该方法内部什么也没做是立即返回的，这点影响真的可以是忽略不计的，我觉得相较之而言，数据库、负载均衡单点等常见的系统性能瓶颈问题往往会更先于此问题出现。


# Java语言设计中的单例模式

在Java语言自身的设计实现中，也随便可见单例模式的身影，现举例如下。


## Runtime

```java
public class Runtime {
    private static Runtime currentRuntime = new Runtime();

    public static Runtime getRuntime() {
        return currentRuntime;
    }

    private Runtime() {}

}
```

Runtime采用了最初的Soup写法，毕竟它是Java运行时必要的对象，也没有延迟加载的必要，直接在类加载时实例化，也不会遭遇线程安全性的问题，很干净且合理。


## Desktop

```java
public class Desktop {
    public static synchronizedsynchronized Desktop getDesktop(){
        if (GraphicsEnvironment.isHeadless()) throw new HeadlessException();
        if (!Desktop.isDesktopSupported()) {
            throw new UnsupportedOperationException("Desktop API is not " +
                                                    "supported on the current platform");
        }

        sun.awt.AppContext context = sun.awt.AppContext.getAppContext();
        Desktop desktop = (Desktop)context.get(Desktop.class);

        if (desktop == null) {
            desktop = new Desktop();
            context.put(Desktop.class, desktop);
        }

        return desktop;
    }
}
```

在Java图型化界面中，Desktop采用了线程安全的延迟加载，这在很大程序上依赖于该类的特性，Desktop是否被支持，包括App的上下文都是要考虑的因素，最后才去创建实例。  
在这里，也并未看到为了synchronized造成的一点性能影响而采用其他写法。


## System.SecurityManager

```java
public class SecurityManager {

    private boolean initialized = false;

    public SecurityManager() {
        synchronized(SecurityManager.class) {
            SecurityManager sm = System.getSecurityManager();
            /* whatever code block */
            initialized = true;
        }
    }
}

public final class System {
    private static volatile SecurityManager security = null;

    public static SecurityManager getSecurityManager() {
        return security;
    }
}
```

这的确是很特立独行的一种写法，可以看到，两个类相互配合共同实现了SecurityManager的单例，并且在System中并未在get函数或是类加载时进行初始化。  
SecurityManager的单例并不是其自身的一个属性，而是在System中，同时，全局唯一访问入口也在System的getSecurityManager方法。  在程序设计上让System持有其他类的实例，并且保证了它是单例的。  

可以注意到，System中该属性使用了volatile修饰，避免多纯种之间的可见性问题，这是为了满足security可以为null的设计需要，这种灵活性是上面的其他例子所没有的。


# 总结

通过思考《Java编程思想》作者介绍单例模式的思路，以及一些写法的改进与讨论，再加上最后Java语言本身的设计实现上的例子，对单例模式可以有更进一步的了解和对实际应用的思考。
单例模式可以实现得很简单，也可以实现得较为复杂，其间的一些取舍与优劣还需诸君在实际应用中考虑具体情况，选择最合适的那一种。


# 参考

1.  [Thinking in Java](https://book.douban.com/subject/2130190/)
2.  [Java8 document](https://docs.oracle.com/javase/8/docs/)
3.  [java-design-patterns](https://github.com/iluwatar/java-design-patterns)
4.  [线程安全的单例类](https://zhuanlan.zhihu.com/p/31046230)

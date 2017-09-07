---
title: "Kindle我的剪帖文件整理脚本"
updated: 2016-07-05 22:39:15
---

＂标注＂是kindle很好用的一个功能。

通常阅读时只管标注，一段时间也读了不少的书，当我想要将所有的标注移入印象笔记的时候，发现该文件里的内容已经变得很多，且各个书标记的内容互相穿插，将标注根据书名放到一起需要一点一点搬运过去，这实在是太麻烦了。
　　

将kindle中的My Clippings.txt文件复制到电脑上，打开后是这个样子的。非常的杂乱无章，我肯定想将月亮和六便士的标注放在一起，**而如果我在这本书中标注了100句话，那我就要进行100次的复制粘贴操作，**才能将它们汇聚到印象笔记中。
这是无法承受的工作量，需要写个脚本，一键模式完成整理。

![](http://osriq34d5.bkt.clouddn.com//17-7-9/31698257.jpg)

根据python字典的可变性及key的唯一性，将书名都提取出来作为key，同一本书的内容作为字符串依次相加，作为最终的值，再依次列出，写入新文件，便可达到目的。


```python
# -*- coding:utf-8 -*-
from collections import defaultdict


def clean_cli():
    with open('my_cliping.txt', 'r') as f:
        shinewords = f.read().decode('utf-8')
        section = shinewords.strip().split("==========\r\n")
        # 传入str作为default_factory.
        books = defaultdict(str)
        for i in section[:-1]:
            i = i.split('\n')
            books[i[0]] += i[3]+'\n\n'

        with open('note.txt','wb') as f:
            for k, v in books.iteritems():
                f.write(k.encode('utf-8') + '\n\n' + 
                    v.encode('utf-8') + '==========\n')


if __name__ == '__main__':
    clean_cli()
```

代码里用到了collections模块中的defaultdict， 是为了处理一个细节。

以书名为key， 标注段落为value时， 有两个行为， 当books中未出现此key时， 是`d[key] = value`。
之后便是`d[key] += value`。

最常规的思路是在for之中进行if判断， 感觉上比较啰嗦。
defaultdict构造时传入一个函数名str，直接构造各key的初始value为空字符串，之后直接加便可以。
当defaultdict传入list为参数时，相应地，for之中可改为append来处理。

除此之外，还有另一种较为简洁的写法是: `d.setdefault(key, {}) += value`。
拒文档所说，其效率不如defaultdict。

运行之后，生成了新的txt文件，效果如图，感觉甚是清爽。
![](http://osriq34d5.bkt.clouddn.com//17-7-9/13224149.jpg)

---
title: 你见过Python的GIL吗
date: 2018.10.19 23:46
tags:
- python
- 并发
---

GIL是**Global Interpreter Lock**的简称，翻译为中文是**全局解释器锁**，维基百科的解释为：

> 全局解释器锁是计算机程序设计语言解释器用于同步线程的一种机制，它使得任何时刻仅有一个线程在执行。即便在多核心处理器上，使用 GIL 的解释器也只允许同一时间执行一个线程。

<!--more-->

# 关于Python多线程与GIL的思考


## 问题的提出

学过Python的人大都知道这个解释性语言最通用的实现(CPython)采用了GIL的方式，因此在网上可以看到一些言论说“Python因为有GIL存在，多线程就算了，还是多进程吧”。   
可这并不符合使用Python编程的实际体验，的确会让人产生一些疑惑。   
Python有其自带的多线程模块，而且著名的爬虫框架[scrapy](https://github.com/scrapy/scrapy)可以同时爬多个网站，感觉上其并没有受到GIL的限制。   
与Java对比的话，Java也支持多线程也可以写爬虫，而Java并没有GIL，这与Python看起来好像没有什么区别，那么GIL到底有没有发挥作用呢？   

能否使用Java和Python分别写一段语义上一样的代码，通过两段程序的output有着明显的不同来证明GIL的确存在并且起了一定的作用呢？   
要做这个事情首先要进行理论上的更进一步探索，才能进行代码的实现与output的设计。


## 关于并发的知识铺垫

<[CSAPP](https://book.douban.com/subject/26912767/)>上提到了三种不同层面的 **并发编程技术**，分别为：

1.  进程级别的并发；
2.  I/O多路复用；
3.  线程级别的并发。

显然此篇的讨论应该归到第三种类型。

接下来，还要明确另一对容易搞错的概念， **并发** 与 **并行** 。  
**并发** 指的是逻辑控制流在时间上的重叠，而 **并行** 则是指对多核CPU的利用。  
并行只是并发的一个真子集，有种说法是“并发是基于逻辑上的同时发生，而并行是基于物理上的同时发生”。  
所以，在只有一个CPU的机器上也可以运行并发程序，却不能运行并行程序。


## 使用加速比证明GIL存在的假设

根据以上关于并发与并行的基本知识，Python与Java在并发程序上的本质区别便可以得知。  
即，因为有GIL的存在，Python无法利用到多核处理器的并行性，但依然可以编写除此之外的并发程序，并获得效率提升。而Java则无此限制。  

CSAPP中提到了对于并行程序性能的衡量标准: **加速比** 。
<div align=center>
![img](https://user-gold-cdn.xitu.io/2018/10/19/1668d04bf3c07dec?w=228&h=108&f=png&s=4216)
</div>
上述公式中，Sp称为加速比，其中p是处理器核的数量，Tp是指在p个核上程序的执行时间，当T1是程序顺序执行版本的执行时间时，Sp称为绝对加速比，而当Sp为程序并行版本在一个核上的执行时间时，Sp称为相对加速比。  

所以，可以使用绝对加速比来证明GIL的存在。
预期是，写一段无IO的计算密集性任务，分别交给Python与Java的一个(顺序执行)、多个线程(并行版本)去运行，算出各自的加速比，如果Python版本加速比小于1，而Java版本的加速比在计算机核心数左右，则说明是GIL起了作用，导致Python程序无法发挥多核的并行性。


# 证明过程

依然使用书中的例子: 做一个加法任务，从0加到0x7fffffff求和，通过设置线程数n，将数字加和任务平均拆分为n份，给到各线程做自己的一份，最后将子任务的和再加和求得最后的结果。  
那么当n等于1时，即为顺序版本，n大于1时则为并行版本。  
书中代码使用C语言实现，此处分别改写为Python与Java两个版本。

入口为：
```python
def main():
    thread_num1 = 1
    thread_num2 = 2
    thread_num4 = 4
    thread_num8 = 8
    print ("sum_task with thread_num1 cost time: " + str(measure_time_cost(thread_num1)) + "s in Python version.")
    print ("sum_task with thread_num2 cost time: " + str(measure_time_cost(thread_num2)) + "s in Python version.")
    print ("sum_task with thread_num4 cost time: " + str(measure_time_cost(thread_num4)) + "s in Python version.")
    print ("sum_task with thread_num8 cost time: " + str(measure_time_cost(thread_num4)) + "s in Python version.")
```

分别用尝试1，2，4，8个线程下运行结果，`measure_time_cost` 主要用来创建目标数量的线程，给各线程分配自己的计算任务，然后等待各线程全部返回，再加和，同时返回耗时，该函数实现为：  
```python
def measure_time_cost(thread_nums):
    nums = 99999999 # Python加到0x7fffffff要太久，改一个小一点的值。
    num_per_thread = int((nums + 1) / thread_nums)
    thread_list = [None] * thread_nums
    task_list = [None] * thread_nums
    start_at = time.time()
    for i in range(thread_nums):
        ct = SumTask()
        thread_list[i] = threading.Thread(target=ct.run, args=(i, num_per_thread))
        thread_list[i].start()
        task_list[i] = ct
    for i in range(thread_nums):
        thread_list[i].join()
    end_at = time.time()
    result = 0
    for i in range(thread_nums):
        result += task_list[i].get_result()
    print (result)
    return end_at - start_at
```

用到的SumTask就是一个简单的类用来处理返回值，不想去用queue，全局变量什么的。  

由于笔者的mac只有两核，无法看到4核、8核等更明显的效果，Python版本的程序跑下来结果为：  
<div align=center>
![img](https://user-gold-cdn.xitu.io/2018/10/19/1668d04bf3b5a99a?w=1058&h=372&f=png&s=66487)
</div>

而Java版本的相同实现，跑下来的结果为：  
<div align=center>
![img](https://user-gold-cdn.xitu.io/2018/10/19/1668d04bf3aebe77?w=697&h=371&f=png&s=64233)
</div>

由于电脑核少，故主要看2核情况的对比，Python版本使用2核并没有得到明显的增速，加速比小于1。而Java版则差不多为2，发挥到了多核的效用，提高了计算密集性任务的效率。  
随着线程数的增加，由于没有那么多核，线程切换的副作用体现了出来，后面时间会增加到比单线程还多。  

之后，在[知乎](https://www.zhihu.com/question/296546864/answer/501359602)上有网友利用8核电脑做了验证，依然与预期相符，Java的最大加速比为0.701/0.168=4.17，而Python的加速比均小于0.5。
<div align=center>
![img](https://user-gold-cdn.xitu.io/2018/10/19/1668d04bf3c7b9a5?w=1278&h=692&f=png&s=583611)
</div>

Java代码就是Executor提交任务，然后通过继承Callable利用Future得到结果。
完整版代码在[这里](https://github.com/guerbai/it-does-works)，直接复制进code runner跑就可以看到结果，很方便。

这，可能是很多人第一次感受到GIL的存在吧~
---
title: "从epoll论io"
updated: 2017-11-25 14:45:00
---

## 起源
写这篇的一个直接原因是去七牛面试时被问到了一个问题：
> 一台性能很好的服务器，如何处理100万个连接并且使其请求不阻塞。

毫无头绪，下来后跟前同事交流发现其考点在于epoll。    
彼时epoll的知识的确没怎么掌握，同时感觉这种事件机制与nginx与node的运行机制均有相似之处，遂想将其搞清楚，通透的话，应该能理解很多事情。

## I/O
一个流可以是文件，socket，pipe等等可以进行I/O操作的内核对象。    
I/O，即读写流。    
I/O过程中涉及到缓冲区(应用程序缓冲区)与内核缓冲区的概念。    
缓冲区的引入是为了减少频繁I/O操作而引起频繁的系统调用, 操作一个流时，更多的是以缓冲区为单位进行操作。

I/O多路复用即为一个进程同时处理多个流的能力。

## 几种I/O模型

**阻塞I/O**    
最简单的情况为同步阻塞I/O。    
一个进程写，另一个进程读，过程中有各种阻塞情况发生。    
是同步的。

**多进程或多线程I/O**    
可以处理多个流，但效率差。

**非阻塞忙轮询I/O**    
对多个流从头到尾问一遍，有事件便处理。    
可以处理多个流，但效率不高。    
若所有流均无事件处理，凭白浪费CPU。

**select**    
为上一种模式引入一个代理，即为select。    
此时，I/O事件不由内核自己处理，而是交给了该代理。    
select可是时观察多个流，当其中有I/O发生时，会将所有流从头到尾过一遍，处理事件。    
若无事件，则会阻塞在select观察处，不会消耗CPU。    
缺点：
1. 观察流的数量有限(1024)；    
2. 发生事件时，遍历所有流，效率低；    
3. fd_set由用户空间拷贝到内核空间，再由内核空间拷贝回用户空间。    

处理时时间复杂度为O(n)，n为观察的流的数目。

**poll**    
poll改善了select的第一个缺点，但性能依然堪忧。    
解决方案是使用pollfd结构而不是select的fd_set结构，可以不受数量限制。

**epoll**    
epoll解决了select的全部三个问题。具体下面细说。


## epoll运作
**机制**    
与select, poll均只有一个函数不同，epoll提供了三个函数：    
int epoll_create;    
int epoll_ctl;    
int epoll_wait;    

参数不用在意，epoll_create创建一个epoll对象。    
epoll_ctl用于往内核的数据结构里塞入或移出socket句柄，socket会以红黑树的形式保存在内核cache里，以支持快速的查找、插入、删除。    
epoll_wait在其监控的所有句柄有事件发生时，进行相应处理。    

可以发现，epoll记下了向其注册的socket句柄的位置，这样，在事件发生时，该事件会被注册到一个就绪设备的队列，在触发(lt or et)时，其只需轮询该队列的数据，然后进行处理即可。    
避免了遍历所有的socket句柄。    

这种机制可以显著提高程序在大量并发连接中只有少量活跃的情况下的系统CPU利用率。    

**复杂度**    
epoll时间复杂度为O(k)，k为发生事件的数目。    
当然，记录下它维护的socket信息及结构，需要更多的空间，这种性能的提高实际上是一个用空间换时间思想的具体应用。    

**解决select的三个问题**    
1. epoll所支持的FD上限是最大可以打开文件的数目，具体数目可以cat /proc/sys/fs/file-max察看，这个数目和系统内存关系很大；    
2. 机制中已说明；    
3. 在调用epoll_ctl时，会发生一次拷贝，每次去处理事件便不用再去做这样的事件。    


**一个具体的例子**    
网卡设备对应一个中断号，当网卡收到网络端的消息的时候会向CPU发起中断请求, 然后CPU处理该请求。通过驱动程序进而操作系统得到通知, 系统然后通知epoll, **epoll通知用户代码**。    

## 水平触发
level triggered.    
只要有数据可以读，不管怎样都会通知。    

## 边缘触发
edge-triggered.    
只有状态发生变化时才会通知，可以理解为电平变化。    

边缘触发的机制是有可能会出错的：    
满足读条件时，去读数据可能存在一次性没有读完的情况，这意味着这次I/O并未结束，而由于该机制仅通知一次，而不管数据是否读取结束，不会再次触发将数据读完。    

边缘触发性能更高，但是使用更加复杂，因为任何意外的丢失事件都会造成请求处理错误。    

如果要使用et方式，那么，应用程序应该注意：    
1、将socket设置为non-blocking方式;    
2、epoll_wait收到event后，read或write需要读到没有数据为止，write需要写到没有数据为止。    

## nginx事件驱动机制    
Nginx就使用了epoll的边缘触发模型。    

## node异步机制    
node核心思想是单线程异步。    
I/O分为网络I/O与磁盘I/O。    
网络I/O层面，node使用了libuv库，而libuv又使用了epoll，固node的网络I/O异步模型是基于epoll的，与nginx一样。    
磁盘I/O层面，则是node引擎内部启多个线程模拟出来的。    

## 进阶阅读    
1. [libuv网络I/O机制](http://luoxia.me/code/2017/07/27/libuv%E7%BD%91%E7%BB%9CIO%E6%9C%BA%E5%88%B6/)    
2. [带你领略Nodejs前世今生](http://www.jianshu.com/p/297f448b7a18)    
3. [Nginx学习之七-模块ngx_epoll_module详解（epoll机制在nginx中的实现）](http://blog.csdn.net/xiajun07061225/article/details/9250341)    


## 参考：    
1. [epoll 或者 kqueue 的原理是什么？](https://www.zhihu.com/question/20122137)    
2. [linux下非阻塞io库 epoll](https://zhuanlan.zhihu.com/p/27050330)    
3. [epoll 水平触发 边沿触发](http://www.cnblogs.com/my_life/articles/3968782.html)    
4. [select、poll、epoll之间的区别总结[整理]](http://www.cnblogs.com/Anker/p/3265058.html)    
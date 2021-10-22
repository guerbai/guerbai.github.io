---
title: Linux发行版与GUI介绍
date: 2021-10-22 16:16:36
tags:
- 软件
- 折腾
---

## GNU/Linux的诞生

1991年8月25日，21岁的[赫尔辛基大学](https://zh.wikipedia.org/wiki/赫尔辛基大学)学生Linus Torvalds发布了他的开源操作系统，"Just a hobby, won't be a big professional thing"，几年后，这个"hobby"--Linux成为了计算机历史上最重要的一个项目。

与Windows这样以盈利的操作系统不同，Linux的理念是：

> Software is like sex; it's better when it's free.     --Linus Torvalds

<!--more-->


时间再回到1983年，AT&T与BSDI正因为Unix打得不可开交([Unix Wars](https://en.wikipedia.org/wiki/Unix_wars))，Richard Stallman创建了GNU(GNU's Not Unix) Project，试图建立可以替代Unix的自由与开源版本操作系统。彼时的Unix已然非常庞大，经过了几年的努力，GNU重写了许多自由软件，其中包括今天耳熟能详的Tar、Bash、Grep等。

到了90年代，GNU项目依然缺少操作系统内核。而一个完整的操作系统需要内核来连接硬件与软件，掌控CPU与内存来运行软件。此时横空出世的Linux，正是GNU所需要的。于是一个完整的替代Unix的操作系统诞生了：GNU/Linux！

## Linux发行版

因为是自由软件，任何人都可以根据自已的喜好定制自已的操作系统，到目前已经有了千级别的Linux发行版。

![](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211020013629.png)

一个Linux发行版包括：

- Linux内核
- 一系列预装软件
- 软件包管理器
- 桌面环境(optional)

各发行版之间有着几大派系和千丝万缕的衍生关系，比如使用apt的Debian家族，基于Debian衍生出了Ubuntu这样对新手十分友好的发行版，而基于Ubuntu又衍生出了Kubuntu、Linux Mint等等。

此外另一大发行版派系是使用rpm/yum的Redhat家族，其中包括作为服务器常用的CentOS，以及著名的Fedora。

事实上，很多Linux发行版都会原生装配一些用户并不会使用的软件包，这不仅占用了电脑的资源，同时也会占用使用者的心力。于是又诞生了两个讲究简单和最小化原则的发行版派系：Arch与Gentoo。



完整的发行版的发展脉络及衍生关系见[维基百科](https://en.wikipedia.org/wiki/Linux_distribution#/media/File:Linux_Distribution_Timeline_Dec._2020.svg)，看到也许会被吓一跳。

## GUI与X Window System

黑乎乎的终端是Linux给人留下的刻板印象，然而作为个人日常使用来讲，用户更喜欢也更需要GUI--用户图形界面。

于是有了X Window System，它通过软件工具及架构协议来创建操作系统所用的GUI，此后逐渐扩展适用到各形各色的其他操作系统上，现在几乎所有的操作系统都能支持与使用X。

X只是工具包及架构规范，本身并无实际参与运作的实体，目前依据X的规范架构所开发撰写成的实现体中，以X.Org最为普遍且受欢迎。

![](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211022150000.png)

X系统采用Client-Server的架构，与直觉不同的是，用户的显示器是服务端，真正在运行的软件是客户端。

理解X与X.Org存在的意义可以举一个最简单的例子：

使用VMWare安装Linux系统后往往所展示的桌面只是中间很小的一块，这时便可以使用X.Org提供的xrandr工具将分辨率设置为1920x1080来占满屏幕。

## 桌面环境

一个桌面环境由多个软件组成，这些软件共享同一个GUI，这些软件提供给用户视窗、文件夹、工具栏、壁纸、图标、拖放服务等内容。不同桌面环境在设计和功能上的特性会赋予其与众不同的外观和感觉。

Linux有几套常用的桌面环境，包括GNOME、KDE、Xfce等，如第二节中描述，桌面环境只是一个发行版的可选部分，同时是可以替换的。一个Linux系统完全可以同时安装多种桌面环境来进行切换。

这些桌面环境也有各自的特点和理念，比如Xfce的：

>  设计为可作为实际应用，快速加载及运行程序，并减少耗用系统资源

**GNOME of Ubuntu**
![GNOME of Ubuntu](https://ubuntuclub.org/uploads/ubuntu-20-04-lts-scaled.jpg)

**KDE of Manjaro**
![KDE of Manjaro](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211022151409.png)

**Xfce of Artix**
![Xfce of Artix](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211022151504.png)

## Window Manager

窗口管理器与桌面环境不同，它只是用来控制窗口位置与外观，不包括设置壁纸、调节音量等能力

各桌面环境都有自己的窗口管理器，比如GNOME的Mutter，Xfce的Xfwm4。它们为打开的软件窗口提供了最小化、最大化、关闭按钮，以及鼠标点击拖动的能力。

![](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211022152216.png)

与上述这些需要使用电脑鼠标控制不同，在Linux用户中还有另外一种非常流行的WM: Tiling Window Manager.

**Bspwm of ArchCraft**
![Bspwm of ArchCraft](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211022152956.png)

使用这样的WM时，打开的软件窗口不会有*关闭*等图标，也无法通过拖拽来移动位置，窗口会自动铺满屏幕并排列好位置，就像瓷砖一样，非常酷炫且高效。



值得一提的是，不需要桌面环境，只用X.Org+WM即可构建出GUI，在这种环境下比如要设置壁纸可以在终端中使用相应的工具xwallpaper，调节音量可以使用PauseAudio，是比较极客的玩法，优点是不会被预装上一堆本不需要的软件，同时会比一个完整的桌面环境占用更少的系统资源。这是一种“简单和最小化原则”的体现。

## 参考

[Why so many distros? The Weird History of Linux](https://www.youtube.com/watch?v=ShcR4Zfc6Dw)

[UNIX传奇(上篇)](https://coolshell.cn/articles/2322.html)

[X窗口系统](https://zh.wikipedia.org/wiki/X%E8%A6%96%E7%AA%97%E7%B3%BB%E7%B5%B1)

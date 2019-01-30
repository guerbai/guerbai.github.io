---
title: 使用Emacs做GTD软件
date: 2018.07.13 01:54
tags:
- 折腾
- GTD
---

作为著名的“操作系统”，Emacs当然可以用来做GTD软件(使用org-mode)。
平心而论，这个方案还是可行的，首先，data放到Onedrive文件夹里就可以实现云备份与多机同步，此外，用户还可以使用它进行自定义的多维度的数据统计，社区甚至还提供了专门的[org-pomodoro](https://github.com/lolownia/org-pomodoro)插件，这么一来番茄工作法也可以施行，在完成一个番茄钟时还可以让电脑发出“叮”的声音，对一个纯文本编辑器来说，这些实在是有点过于强大了。

<!--more-->

此篇介绍一下如何使用Emacs做GTD软件，里面有一些微小的经验与细节，讲实话这种方案上手难度还是蛮大的，只推荐给想要装B的同学、闲得蛋疼的同学或者本身使用Emacs而尚未使用时间管理的同学实用。

## 原材料
* [最新版Emacs](https://www.gnu.org/software/emacs/download.html);
* [Spacemacs配置文件](http://spacemacs.org/);
* [org-pomodoro插件](https://github.com/lolownia/org-pomodoro)

我使用的Emacs是25.3版本，在装Spacemacs过程或者org-pomodoro插件过程中可能会碰到一些问题，如何成功安装这些原材料并不在本篇准备讲述的范围之内，请参考各自文档，应该都比较容易解决掉的。
Spacemacs与org-pomodoro非必选，仅使用原生的Emacs经过简单的配置即可作为GTD使用，使用配置文件会使整个体验更好，但上手难度相对来说更大了一些，而pomodoro仅提供番茄工作法的支持，若不需要的话亦可不选择。

如果这些问题便没有耐心去解决或者觉得浪费时间，那么说明本方案不适合你，还是及早收手为好。

## 设置data目录
使用GTD软件肯定是要产生一定的用户数据的(之后称用户数据为data)，那么它一定要被放在某个地方，为了云存储、多机同步的目的，可以选择在Onedrive文件夹下建立org目录来存放data。

由于配置不是三两行就能写完的，故专门建立一个文件夹做GTD的配置，编辑配置文件~/.emacs，使Emacs自动加载它时载入GTD的配置文件：
```elisp
(load-file "~/my-agenda.el")
```
在配置文件中，指定data的存放目录，并绑定进入agenda的快捷键，这里配置为Ctrl-C a来触发：
```elisp
(setq org-agenda-files '("~/OneDrive/org"))
(global-set-key (kbd "C-c a") 'org-agenda)
```
经过这几行配置，已经初有效果了：
<div align=center>
![](https://upload-images.jianshu.io/upload_images/11528373-8a4a2d34d7a75f2a.gif?imageMogr2/auto-orient/strip)

通过Ctrl-C a进入agenda view
</div>

进入agenda-view后，可以看到一些操作提示，通过一个按键可以快速查看一天、一周、所有、关键字搜索、标签搜索等任务。
## 新增任务
配置好data目录后，再配置具体要将信息写于哪个文件，可以配置多个文件，出于简化，这里将所有的agenda todo写入~/OneDrive/org/todo.org文件下。
```elisp
(setq org-default-notes-file "~/onedrive/org/todo.org")
(global-set-key (kbd "C-c r") 'org-capture)
```
上面设置的快捷键C-c r，Emacs会提示根据todo template来创建一个任务。
<div align=center>
![](https://upload-images.jianshu.io/upload_images/11528373-69515af172a51d58.gif?imageMogr2/auto-orient/strip)

新建一个任务
</div>

创建任务之后，可以在agenda-view的list all TODO entries里看到刚刚添加的任务。
<div align=center>
![](https://upload-images.jianshu.io/upload_images/11528373-9804a06d2b939273.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

all todo entries
</div>

但是这是在日任务、周任务里是看不到的，需要为它添加起始、结束时间，操作分别为C-c C-s，C-c C-d。
<div align=center>
![](https://upload-images.jianshu.io/upload_images/11528373-b3628f8a912c1dc2.gif?imageMogr2/auto-orient/strip)

为任务添加起始、结束时间并在week中查看
</div>

## 配置任务Template
见上面新建一个任务时的图，新建任务是基于Template的，我们利用比如大写的TODO字样是Emacs自带的Template。同时，org-agenda支持用户配置自己的template。

在配置中加入如下代码，可以增加时间管理中充当*收集篮*角色的template：
```elisp
;; capture;
(setq org-capture-templates
      '(("t" "Todo" entry (file+headline org-default-notes-file "待办事项")
         "* TODO %?\n  %i\n  %a")
        ("s" "收集篮" entry (file+headline org-default-notes-file "Quick notes")
         "* Quick notes %?\n %i\n %a")
        ))
```

![](https://upload-images.jianshu.io/upload_images/11528373-2d76be130d876353.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/11528373-d6fd70fd3cc7cf6f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

利用这个机制，可以编写自己的template，对自己的使用情景进行分类，可以使操作更加多样化，满足更大的想象力。

## 周期性任务
有些任务是周期性、经常没有结束的，比如我使用RSS看各种资讯，每3天看一次，时间在当天中午吃过饭13:00到14:00一个小时，那么可以在设置任务起始时间时，加入周期性的标记即可（在指定的时间后面加上：+3d），效果在week-view中很明显，会周期性地出现。

![](https://upload-images.jianshu.io/upload_images/11528373-0a472590c645d05b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](https://upload-images.jianshu.io/upload_images/11528373-a3e90d2051cb52aa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 按Tag进行分组与搜索
使用Tag进行将事物进行分组是一种常见的管理模式，在org-agenda中，新建一个任务时可以为它加Tag，方法为在任务描述后面加上`:tag1:tag2:`这样的标记。

![](https://upload-images.jianshu.io/upload_images/11528373-d1ef935cf664cc1e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在上图中可以看到，将*学agenda*归为*学习*和*工具*标签下，这样，就可以通过标签搜索的功能将该Tag下所有的任务搜出来。

![](https://upload-images.jianshu.io/upload_images/11528373-189ce75856c938db.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

<div align=center>
![](https://upload-images.jianshu.io/upload_images/11528373-899e3c3462713157.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

分别按不同的标签搜索
</div>

同时，agenda-view还提供各种搜索的方式，可以根据关键字，是否完成等条件搜索。
各个搜索入口在agenda-view描述得很清楚：
<div align=center>
![](https://upload-images.jianshu.io/upload_images/11528373-fc936d20a9a9e203.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

agenda-view按键说明
</div>

## 任务优先级
根据四象限工作法，各任务是有优先级的，org-agenda当然提供了为任务设计不同优先级的功能，为A，B，C三个不同的级别，操作为将光标放到任务的一行上，按Shift-上、下键，即可调整该任务优先级。
<div align=center>
![](https://upload-images.jianshu.io/upload_images/11528373-6679f946b02642b0.gif?imageMogr2/auto-orient/strip)

切换任务优先级
</div>

如果觉得自带的ABC不够用的话，还可以自己定义优先级，配置如下：
```elisp
(setq org-highest-priority ?A)
(setq org-lowest-priority  ?D)
(setq org-default-priority ?D)
(setq org-priority-faces
      '((?A . (:background "red" :foreground "white" :weight bold))
        (?B . (:background "DarkOrange" :foreground "white" :weight bold))
        (?C . (:background "yellow" :foreground "DarkGreen" :weight bold))
        (?D . (:background "DodgerBlue" :foreground "black" :weight bold))
        ))
```
上述配置定义了最低优先级为D，且为默认优先级，同时设置了颜色，使得各优先级区分度更高，配置过后效果图如下：
<div align=center>
![](https://upload-images.jianshu.io/upload_images/11528373-0f812b13843c0114.gif?imageMogr2/auto-orient/strip)

有底色与自定义优先级的展示
</div>

## 获取Chrome链接
有一种常见的场景为在浏览网页时看到一篇文章一时看不完，要把它记下来之后再看，这个时候需要复制链接，再粘贴到Emacs中，这个过程比较烦人，牛人子龙山人为此提供了如下的配置，通过AppleScript，再增加一个相应的Template，可以使新增该Template的任务时自动去Chrome抓取url并粘贴在Emacs中，可以说是非常神奇了。

```elisp
(defun my/insert-chrome-current-tab-url()
  "Get the URL of the active tab of the first window"
  (interactive)
  (insert (my/retrieve-chrome-current-tab-url)))

(defun my/retrieve-chrome-current-tab-url()
  "Get the URL of the active tab of the first window"
  (interactive)
  (let ((result (do-applescript
                 (concat
                  "set frontmostApplication to path to frontmost application\n"
                  "tell application \"Google Chrome\"\n"
                  "	set theUrl to get URL of active tab of first window\n"
                  "	set theResult to (get theUrl) \n"
                  "end tell\n"
                  "activate application (frontmostApplication as text)\n"
                  "set links to {}\n"
                  "copy theResult to the end of links\n"
                  "return links as string\n"))))
    (format "%s" result)))

;; capture;
(setq org-capture-templates
      '(("t" "Todo" entry (file+headline org-default-notes-file "待办事项")
         "* TODO %?\n  %i\n  %a")
        ("s" "收集篮" entry (file+headline org-default-notes-file "Quick notes")
         "* TODO %?\n  %i\n %U"
         :empty-lines 1)
        ("c" "Chrome" entry (file+headline org-default-notes-file "Quick notes")
         "* Later see: %?\n %(my/retrieve-chrome-current-tab-url)\n %i\n %U"
         :empty-lines 1)
        ))
```
效果如下：
<div align=center>
![](https://upload-images.jianshu.io/upload_images/11528373-22859246212acd4b.gif?imageMogr2/auto-orient/strip)

自动抓取Chrome url创建任务
</div>

## 统计
使用Emacs可以对任务完成情况及时间使用情况进行统计。
对各Tag、各种类型的任务的耗时进行统计，统计出来的结果可能是一个人意想不到的（比如竟然在重要的事情上花的时间不及不重要却相对简单的事情的时间的一半），这种统计对之后的时间安排有导向性，在时间管理中还蛮重要的。

开始一个任务时的操作被称为clock in，结束计时被称为clock out，操作分别为C-c C-x C-i与C-c C-x C-o，在一个任务上可多次计时，最终Emacs会自动处理总的时间。

在todo.org文件下，C-c C-x C-r可以生成一个动态的报表，之所以称为动态，意思是它生成一次，就呆在那里，下次来看，可以会根据之间的变化进行统计值的更新，手动刷新操作为C-c C-c。

C-c C-x C-r命令会生成一个org中的代码块，可针对各种关心的维度，比如各tag，各优先级等，进行统计项的筛选，每个相同的统计表保留一份即可。

由于我已经好久没有用这个东西统计了，没有数据，这里盗[一个网上的图](https://www.zhihu.com/question/34299750/answer/58303458)，来说明这个功能的强大。
<div align=center>
![](https://upload-images.jianshu.io/upload_images/11528373-733b86af5fdc764c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

统计图示例
</div>

上面clocktable后面的:maxlevel :scope等均为筛选项，具体参数及用法见[文档](https://orgmode.org/manual/The-clock-table.html#The-clock-table)，可以构造自己关心的统计表格，并且随时更新哟！

## org-pomodoro
番茄工作法是一个著名的专注高效的GTD实践，org-pomodoro插件可以提供一个25分钟（可自定义）的倒计时器，到时间会提醒你休息一下，然后再吃下一个番茄。

安装好插件后，要为一个task开启一个番茄钟，只需要在task上M-x: org-pomodoro就开始了：
<div align=center>
![](https://upload-images.jianshu.io/upload_images/11528373-98f4c5a447f38632.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

tab栏上的倒计时钟
</div>

一声“叮”响之后，这个番茄钟就结束了，会进入break阶段：
<div align=center>
![](https://upload-images.jianshu.io/upload_images/11528373-fc9fe0ddd5114c08.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

break5分钟
</div>

如果要关掉一个误打开的番茄钟，使用S-M: (org-pomodoro-kill)。

## 做项目管理
有篇很棒的使用org做项目管理的文章，我觉得已经算是很好的实践了，在此处分享一下。
[Behind the code: project planning](https://www.devalot.com/articles/2008/07/project-planning)

***
以上是所有功能的展示充分说明了Emacs有能力作为一个GTD软件并且在某些方面还要做得比其他好，但缺点也较明显，上手难度太大，要记的快捷键太多，有些点过于原始，要熟练应用还需要一段不小的时间适应与折腾，在长处和缺点之间要综合考虑。
这一趟总结下来，有很多地方之前都用过但现在已经不记得了要再去查，费了不少的时间，但这对我而言也是一次较全面的巩固。

有趣的是，这么一番总结下来，感觉自己又有一点想用Emacs了，毕竟还是酷的呀。

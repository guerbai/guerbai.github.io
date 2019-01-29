---
title: 使用 Karabiner 改善 Poker 键盘体验
date: 2018-10-23 12:00:00
tags:
- 软件
- 折腾
---


Poker 键盘以其小巧、精致、可编程深受广大用户的喜爱，更关键的是，它颜值还很高。时常作为 Mac 的外接键盘日常使用。  



![请输入图片标题](https://cdn.sspai.com/2018/10/25/3a6b07ce1f3f2a8b3928fa269958cd01.png)


<!--more-->

然而往往小巧与极客的事物便意味着会有一些操作方式让使用者不够习惯，因而会产生一些痛点，比如没有直接的方向键等等。  



网上有一些文章介绍了 Poker 底部开关的设置，以及 Mac 基本的几个功能键修改功能，笔者进行过尝试，然而其修改过于基础，依然不够好用。  



本篇介绍了笔者使用 Mac 上的改键软件 [Karabiner](https://pqrs.org/osx/karabiner/) 对 Poker 键盘进行自定义化设置，从而优化其作为 Mac 外接键盘体验的具体实施方案。  



通过本文所举的 case，掌握了 Karabiner 的使用方法之后，便可以对任意键盘进行任意程度的自定义设置了，可谓一通百通，解放你的手指，在 Mac 上驰骋，效率提升一个数量级。





## 功能键的调整



功能键一般要左手去按，Poker 左下角的功能键布局如图所示：  



![请输入图片标题](https://cdn.sspai.com/2018/10/25/0778e093a41654521ba52d87351b1950.png)



### 调整左 Ctrl 与左 Command



位于键盘最左下角的键按键方式是使用 **左手掌外侧** 按下，这样不需要移动扭曲小指或是移动手在键盘上的位置，可减少对手指的伤害，非常自然。  



然而，Poker 最左下角的键是 Ctrl，而在 Mac 系统上，最常用的 *保存、复制、粘贴* 三个操作的按键却是 `⌘Command + S \ C \ V` 来实现的。  



左 Command 键位于左 Ctrl 右边，依然使用左手掌外侧来按，但这就不那么自然了，需要左手下部往右侧稍稍移动一个键位来够到。  



根据频次来讲，在 Mac 上，使用 `Ctrl + Key` 组合键的常用操作不能说没有，但远比不上上述保存、复制、粘贴三兄弟，因此，果断将二者调换位置。  





### 将 Capslock 改为左 Option



笔者没有使用 Capslock 的需求，大写字母通过 `⇧Shift + A` 这样的方式来实现，完全可以将它替换为更常用的按键。  



在 Mac 上，使用 Option 的频次较多的操作主要有两个，唤起 Alfred 用 `⌥Option + Space` 的快捷键，以及在 Emacs 中运行函数用 `⌥Option + X` 的快捷键。  



而在 Poker 上左 Option 位于左 Command 的右侧，左手掌移一个键已经够难受了，移两个键更是不可取，若使用大拇指去往里勾，笔者认为和使用小指去勾 Ctrl 一样，长久而言对手指有损伤，故果断将 Capslock 改为左 Option，这样对于上述所提到的两个操作都方便与自然了许多，使用小指从 A 移到 Capslock 是很轻松的事。  



![请输入图片标题](https://cdn.sspai.com/2018/10/25/fdd15e5d930ef73ccb8bc62515ac2e23.png)



## 进阶设置





### 方向键的改进



Poker 并无自带的方向键，然而就算自带方向键，将右手抬起来去按这个操作还是蛮糟心的，况且还容易按错。  



Poker的原生方案是 `Fn + W \ A \ S \ D`，这当然很极客了，然而这却也是笔者使用 Karabiner 的直接原因。  



问题在于这个操作需要两个手，而通过自定义 Karabiner 的 Complex Modifications，可以将 `Fn + W \ A \ S \ D` 这种方案改为 `⌥Option + W \ A \ S \ D`，加上之前将 Capslock 改为了 Option，则仅使用左手便可以使用方向键。  



Complex Modifications 是 Karabiner 的一个进阶功能，通过 json 配置的方式，可以实现任意的键盘行为方式的自定义，绝对超出你的想象。  



官方提供了 [一些例子](https://pqrs.org/osx/karabiner/complex_modifications/)，比如将 Capslock 进行修改，当它与其他键一起使用时发挥 Ctrl 的功能，当它单独被按下时，发挥 Esc 的功能。  



这些例子中并没有更改 Poker 方向键的 case，然而通过参考其例子的 json 配置方式，完全可以实现自己想要的任何行为。  



其配置文件在 `~/.config/karabiner/assets/complex_modifications` 目录，新建`guerbai-keymap.json` 文件，内容如下：


```json
    {
        "title": "poker arrow keys",
        "rules": [
            {
                "description": "holing left alt and asdw use arrow keys.",
                "manipulators": [
                    {
                        "type": "basic",
                        "from": {
                            "key_code": "a",
                            "modifiers": {
                                "mandatory": ["left_Option"]
                            },
                            "Optional": ["any"]
                        },
                        "to": [
                            {
                                "key_code": "left_arrow"
                            }
                        ]
                    }
                ]
            }
        ]
    }
```


以上只举了将 `⌥Option + A` 改为左方向键的配置，配置的 key 是自解释的，即当 A 被按下时，若此时 Option 也是被按下的，则实现 `left_arrow` 的行为，很易懂就不再多解释，同样的格式在 rules 里来四份分别对应 `W \ A \ S \ D` 到四个方向键即可。





### Backspace 与 Enter



在使用 Evernote 等软件编辑文字或浏览网页时，通常是右手握鼠标，左手在键盘，这个过程中通常会遇到要按 Backspace 或 Enter 的情况，这时便不得不将右手从鼠标拿开，去按退格或回车，再放回到鼠标上，极其不爽。  



在上述姿势下，自然可以想到若是左手可以直接按到 Backspace 与 Enter 的话便会方便许多。  

这里的配置与方向键的改进很像，笔者采取的策略是，当 Option（已被改到 Capslock）被单独按下时，呈现出 Backspace 的作用，而 `Command（已被改为左 Ctrl）+ Space` 则呈现为 Enter。配置如下：


```json
{
    "title": "poker arrow keys",
    "rules": [
        {
            "type": "basic",
            "from": {
                "key_code": "spacebar",
                "modifiers": {
                    "mandatory": ["left_Command"]
                },
                "Optional": ["any"]
            },
            "to": [
                {
                    "key_code": "return_or_Enter"
                }
            ]
        },
        {
            "type": "basic",
            "from": {
                "key_code": "left_Option",
                "modifiers": {
                    "Optional": ["any"]
                }
            },
            "to": [
                {
                    "key_code": "left_Option"
                }
            ],
            "to_if_alone": [
                {
                    "key_code": "delete_or_Backspace"
                }
            ]
        }
    ]
}
```




## 左右切换全屏程序



Mac 触控板的四指横扫是切换全屏程序的利器，而外接键盘却并不那么方便。`⌘Command + Tab` 自然是一种方案，然而却不够精确，同时要反向切 `⌘Command + ⇧Shift + Tab` 是极难按的，笔者通常更喜欢使用 `⌘Command + 方向键` 来进行切换。  



在未改造方向键时，这个操作在Poker上简直麻烦，需要左手掌外侧压住 Command，右手掌外侧压住 Fn，左手指按 A 或 D，然而上述改方向键的方案并不能直接与 Command 配合来进行切换，因为它仅指定了 mandatory 为 Command，还需要进一步改造。  



笔者的设计是将这个操作改为左手一只手可以进行，使用 `⌘Command + ⌥Option + A \ D`  来进行切换，这样比如在网页上看到一段话，可以右手用鼠标进行复制，左手切到旁边的 Evernote，右手鼠标点击选择笔记，左手粘贴，不需要做任何大幅度的移动。  



在上述 Karabiner 配置文件夹下再建一个文件命名为 `guerbai-change-application.json`，内容输入：


```json
{
    "title": "change application",
    "rules": [
        {
            "description": "change application use poker",
            "manipulators": [
                {
                    "type": "basic",
                    "from": {
                        "key_code": "a",
                        "modifiers": {
                            "mandatory": [
                                "left_Option",
                                "left_Command"
                            ]
                        },
                        "Optional": [
                            "any"
                        ]
                    },
                    "to": [
                        {
                            "key_code": "left_arrow",
                            "modifiers": [
                                "left_Command"
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}
```


可以注意到将 mandatory 改为 Option 和 Command，这样就可以仅使用左手方便地切换程序了。



设置界面如下图：



![请输入图片标题](https://cdn.sspai.com/2018/10/25/e0b3cf4c91b4d3abbe1195eb981dad5e.png)



## 最后



相信经过上述示例，已经可以体会到 Karabiner 的强大了，通过简单而又强大的 json 配置，来实现任意键盘上任意自己想要的行为，简直不要太爽。  



[这里](https://gist.github.com/guerbai/2d3d98f6409452d5951ac4aa0e735b2f) 是上述配置的完整版，放到配置文件夹下后，使用 Complex Modifications 的 「Add rule」 添加文件使其生效即可。
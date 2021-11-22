---
title: Suckless--极简主义者的Linux世界
date: 2021-11-06 16:54:51
tags:
- 软件
- 折腾
---
看DistroTube和Luke Smith的Linux视频时被他们高效简洁而炫酷的桌面与窗口操作惊到了，经过一些小小的研究了解到了Tiling Window Manager以及Suckless系列软件。

![](https://raw.githubusercontent.com/guerbai/scene/main/blog/20210930011909.gif)

本文描述了如何安装Suckless系列软件，以及如何在其dwm窗口管理器下基本生存🪵
<!--more-->

## Suckless

[suckless.org](https://suckless.org/)是一个社区，我喜欢称之为“没毛病组织”😂，他们的极简主义哲学是：

> 软件应该简单、清晰、最小化、可用。

简单是Linux的哲学的核心，该组织认为当今的众多软件过于复杂和缓慢，于是开发了一系列的软件来证实这种普遍现象并不是必须的。这些软件主要面向有一定经验的进阶用户，使每个用户都可以定制自己的实际工作场景workflow。

主要包括以下几个作品：

- st(simple terminal)，X环境下的终端
- dwm，动态窗口管理器
- dmenu，用户自定义菜单，程序启动器
- surf，浏览器
- ...

## 安装与启动

首先准备一个Linux发行版，本文以[Garuda KDE Dr460nized](https://garudalinux.org/downloads.html)演示：

![](https://garudalinux.org/images/garuda/download/dr460nized/garuda-dr460nized.webp)

Garuda是一个基于Arch Linux的发行版，下文中提到的一些安装选项亦是基于pacman包管理器，在其他发行版下需要更换为相应的包管理器。

下载几个软件源码到本地：

```sh
mkdir ~/suckless
cd ~/suckless
git clone https://git.suckless.com/dmenu
git clone https://git.suckless.com/st
git clone https://git.suckless.com/dwm
```

suckless软件的一个特点是只提供源码，需要用户自己使用编译安装。某些更轻量级的发行版可能会没有make命令，需要先手动安装相关依赖。

```sh
cd ~/suckless/st
sudo make clean install

cd ~/suckless/dmenu
sudo make clean install

cd ~/suckless/dwm
sudo make clean install
```

三次make命令后几个软件便已成功安装到了系统中。st是dwm环境下的默认终端，dmenu是dwm下的程序启动器，进入dwm之前需要先安装st或dmenu，否则会在dwm中寸步难行。

打开Garuda的默认终端konsole，输入dwm启动。会遭遇`dwm: another window manager is already running`

![](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211106162624.png)

在[Linux发行版与GUI介绍](https://guerbai.github.io/2021/10/22/linux-gui-wm/)中介绍了WM与DE的关系，这是由于当前处在Garuda的桌面环境中，KDE自己的WM已经在运行，无法打开dwm。

这里需要为dwm编写启动选项，使得在登录时(login manager，Linux的一个软件)启动dwm而不启动KDE桌面环境。

```conf
[Desktop Entry]
Encoding=UTF-8
Name=dwm
Comment=Dynamic Window Manager
Exec=/usr/local/bin/dwm
Icon=
Type=Application
```

将上述内容命名为dwm.desktop保存到`/usr/share/xsessions`目录下，退出当前用户登录状态来到登录界面。左下角(其他发行版可能在其他位置)出现了选项，选择**dwm**后输入密码登录。

![](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211106162642.png)

![](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211106162656.png)

于是便来到了“没毛病老哥们”提供的极简主义者的Linux世界。

## 基本操作

```txt
    +------+----------------------------------+--------+
    | tags | title                            | status +
    +------+---------------------+------------+--------+
    |                            |                     |
    |                            |                     |
    |                            |                     |
    |                            |                     |
    |          master            |        stack        |
    |                            |                     |
    |                            |                     |
    |                            |                     |
    |                            |                     |
    +----------------------------+---------------------+
```

dwm的区域分为如上几块，上面是状态栏，包括tags、title以及status；屏幕主要区域分为master与stack区域新打开的窗口会占据master，之前的窗口以栈的方式上下排列在stack区。

![](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211106162823.png)

下面的列表一些dwm环境下的一些快捷键。

| Keybinding                 | Action                                             |
| -------------------------- | -------------------------------------------------- |
| SHIFT+ALT+ENTER            | 打开st                                             |
| SHIFT+ALT+q                | 退出dwm，回到login manager                         |
| ALT+p                      | 打开dmenu，之后可以输入软件名比如firefox来启动软件 |
| ALT+j/k                    | 切换打开的多个window                               |
| SHIFT+ALT+n(1-9)           | 移动当前window至tag n(默认9个tags)                 |
| SHIFT+ALT+c                | 关闭当前window                                     |
| ALT+ENTER                  | 切换某当前window为master window                    |
| ALT+m/t                    | 切换当前window为全屏/切换回来                      |
| ALT+n(1-9)                 | 进入tag n                                          |
| CTRL+SHIFT+PAGEUP/PAGEDOWN | zoom in/zoom out                                   |
| ALT+b                      | toggle status bar                                  |

## 该如何...

dwm下鼠标几乎变得没有作用，在桌面环境中的点击音量按钮调节系统音量等操作变得不再可行，geek们的做法是使用命令行工具，本节给出一些具体场景下的一种可行操作方式。

**浏览图片**

命令行安装sxiv，进入图片所在文件夹，输入：`sxiv *`，可以使用鼠标点击左右切换当前展示图片。

![](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211106162722.png)

**设置壁纸**

命令行安装xwallpeper，确定希望设置的图片路径，比如`~/.config/wall.png`

```sh
xwallpaper --zoom ~/.config/wall.png
```

![](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211106162909.png)

**调节音量**

命令行安装pauseaudio，下列命令是几种对音量可能会做的操作：

| Command                      | Action         |
| ---------------------------- | -------------- |
| pactl set-sink-volume 0 +20% | 音量增加20%    |
| pactl set-sink-volume 0 -20% | 音量减少20%    |
| pactl set-sink-mute 0 toggle | 静音切换       |
| pactl get-sink-volume 0      | 获取当前音量值 |

**截图**

命令行安装scrot，打开dmenu输入`scrotv`即可对当前桌面截图保存在当前文件夹。

若想截图特定窗口，可以加`-s`参数后用鼠标点击想要的窗口。其他具体指令的使用说明见scrot文档。

## st体验优化

st的实现只有2000多行C代码，自身的功能非常有限，以至于各种用户“习以为常”的能力它都没有，包括复制/粘贴、滚动等功能都是默认不支持的，毕竟"simple"。

suckless的软件不提供配置文件，所有配置项均在其源码config.def.h中，修改后需要运行`sudo cp config.def.h config.h && sudo make clean install`重新编译安装。

**复制/粘贴**

在`~/st/config.def.h`的ShortCut中新增两行：

```C
{ MODKEY, XK_c, clipcopy,  {.i=0}},
{ MODKEY, XK_v, clippaste, {.i=0}},
```

重新安装，即可以在st中使用SHIFT+CTRL+c/v来实现复制/粘贴功能。

**emoji**

st自然也不支持emoji的显示，比如[ohmyarch](https://github.com/guerbai/ohmyarch)的README.md中有🤣，运行`cat README.md`会导致st直接crash掉，这里需要一个特定的依赖来解决此问题：

```sh
yay -S libxft-bgra
```

**透明化**

设置了漂亮的壁纸后将终端做一定程度的透明化是一种视觉上的享受。

命令行安装picom，配置文件写于~/.config/picom/picom.conf

```
opacity-rule = [
"90:class_g = 'st-256color'"
];
wintypes:
{
normal = { blur-background = true; };
splash = { blur-background = false; };
};
# Fading
fading = false;
fade-in-step = 0.07;
fade-out-step = 0.07;
```

然而st自身的源码不支持透明显示，suckless提供了一些patches来增强它的功能，类似于其他软件中的插件。

复制[alpha patch diff](https://st.suckless.org/patches/alpha/st-alpha-0.8.2.diff)至st源码目录内，运行`patch < st-alpha-0.8.2.diff`后依然是重新编译安装。然后运行`picom -b`即可实现透明效果。

![](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211106162939.png)

除了alpha外，suckless还提供了其他许多的[patches](https://st.suckless.org/patches/)来扩充功能，感兴趣可以继续探索。

## dmenu的想象力

在path下的可执行文件均可被dmenu找到并运行，用户可以自行编写shell脚本置于`/usr/local/bin`文件夹下由dmenu执行。

比如实现一个关机/重启选项的简单例子：

```sh
choices="shutdown\nreboot"

chosen=$(echo -e "$choices" | dmenu -i -p "Operation:")

case "$chosen" in
    shutdown) shutdown;;
    reboot) reboot;;
esac
```

将该文件保存为sysop.sh置于PATH路径中，即可在dmenu中选择sysop这个选项并进行下一步选择。

这个脚本本身没有太多实际意义，然而有了这样的机制，其实可以实现非常非常多的功能，比如调节音量、浏览切换壁纸、快速打开浏览器标签页等等，笔者认为其定制能力与想象力要比MacOS下的Alfred要更为丰富。

## dwm状态栏

默认的dwm状态栏非常朴素，status部分只显示了`dwm-6.2`，“没毛病老哥”们提供了一个基础的改变status显示内容的机制，比如想要把`dwm-6.2`改变为hello world那么需要运行：

```sh
xsetroot -name "hello world"
```

有了这个简单的机制，便可以通过其他软件比如pauseaudio拿到当前音量信息并展示到status bar；通过date软件拿到当前时间信息并展示。

suckless官网列出了一些他人配置好的[dwm状态栏列表](https://dwm.suckless.org/status_monitor/)，可以参考选用。

![](https://raw.githubusercontent.com/guerbai/scene/main/blog/20211106160407.png)

## What's Next

许多有经验的Linux用户都有自己的suckless软件版本，开箱即用，可以尝试使用一下他们的成熟配置进一步感觉suckless软件的魅力：

- [ohmyarch](https://github.com/guerbai/ohmyarch)
- [DistroTube](https://gitlab.com/users/dwt1/projects)
- [Luke Smith](https://github.com/LukeSmithxyz)
- [TheNiceBoy](https://github.com/theniceboy)


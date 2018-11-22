---
title: 编写Java code时的Util方案
date: 2018-05-08 12:00:00
tags:
---

## 起

Java这种静态语言使用IDE写起来比较有安全感 ，看到各种提示错误即时修改即可。   
有时过多的声明或原生提供的方法又让人感觉写起来有些繁杂。   

由于懒以及个人对代码整洁程度的一点点洁癖，会寻找一些简易的方法来改善这些编码过程中的不爽，而这篇便用来记录这些解决常见问题的Util方案。   
不止包括代码抽象层面，亦有IDE的使用技巧与一些辅助功能性类的介绍。   

由于现在进度还没有越过第一章，随着项目的进行，此篇亦会持续更新。   


## 打印

这个项目要做很多题，经常要使用打印来证明程序的正确性以及效果。   
而Java的打印要使用\`System.out.println()\`方法，是我见过的语言中打印方法编写字数最长的一个，尽管JS的\`console.log()\`已经够恶心了。   
可能还是我孤陋寡闻了吧。   

解决方案很简单，写一个Print类，提供一个静态的print方法，在该方法中再调用Java原本的打印。   
其他地方\`static import\`即可，而作为编写人员，Intellij更是使我不用编写该import语句，直接调用，然后\`ALT+ENTER\`快捷键即可，方便很多。   

    import java.io.PrintStream;
    
    public class Print {
    
        // Print with a newline:
        public static void print(Object obj) {
            System.out.println(obj);
        }
        // Print a newline by itself:
        public static void print() {
            System.out.println();
        }
        // Print with no line break:
        public static void printnb(Object obj) {
            System.out.print(obj);
        }
        // The new Java SE5 printf() (from C):
        public static PrintStream
            printf(String format, Object... args) {
            return System.out.printf(format, args);
        }
    }

该类的实现来自于[Java编程思想 （第4版）](https://book.douban.com/subject/2130190/)，而这种写Util类的思想，不仅在Java，在任何语言的编码中，应该都很常用。   


## 记录时间运行时间

第一章的排序算法对时间是有要求的，10s以内即认为可行。   
课后练习又有一些不同实现，以及它们的运行时间比较。   
如何记录Java程序的运行时间呢？   

我采用最简单的方法：   

    public class CheckSpaceAndTime {
    
        public static void main(String[] args) {
            long startAt = System.currentTimeMillis();
            // algorithm code here.
            long endAt = System.currentTimeMillis();
            print("Program cost time: " + (float)(endAt-startAt)/1000 + 's');
        }
    }

使用System类调用currentTimeMillis()方法可得当前时间戳，单位为毫秒。   
endAt与startAt相减可得结果，进行有意义地打印。   

这依然不够优雅，每个要检查时间的方法，都要在它的开始和结束插入这几句，真的是一点都不clean。   
而且每次都要将这几句代码复制来复制去，烦得不行。   

我希望达到像Python的装饰器一样的效果，打印运行时间不会侵入到算法实现函数的运行。   
比如这样：   

    @print_cost_time
    def main():
        # code here
        return

Java是设计模式的“重灾区”，很Javanic的实现方法可能是装饰器模式，同时又在Java编程思想中看到了代理模式的一个实现，可能也可以处理这种情况。   
具体实现等那本书消化好了再来改进。   

目前采用一个折中的办法，使用Intellij的live template来自动生成一个带有这几行代码的main方法，至少可以省去复制的功夫。   
在IDE的设置页面，搜索live template，点击右边的+号，会在user的命名空间下，增加一个live template。   
此处缩写给maint，选择context为Java。   
如图：   
![img](https://ws1.sinaimg.cn/large/0073xHwmgy1fxee256xt8j31ue146wna.jpg)   

Apply以及OK后，在Java类中，输入maint按tab即可生成上面的代码。   


# 检查对象占用的内存空间

网上查找了一些方法，大都不怎么好用，而且不够clean，用起来很不爽。   
更有甚者，搞了好大一会儿终于跑起来后，发现它查到的只是该对象的引用所占用的空间而不是该对象在栈或堆上占用的空间。   
曾一度以为Java并没有一个for human的对象内存查看工具包。   

而，柳暗花明又一村，这一村是Apache的RamUsageEstimator包。   
为使用它，强行将项目改成了maven管理。   
pom.xml中导入：   

    </dependencies>
    <dependency>
      <groupId>org.apache.lucene</groupId>
      <artifactId>lucene-core</artifactId>
      <version>4.2.0</version>
    </dependency>
    </dependencies>

然后开箱即用，正是我想要的东西：   

    public class CheckSpaceAndTime {
    
        public static void main(String[] args) {
            long startAt = System.currentTimeMillis();
            ArrayList<Integer> s = new ArrayList<>();
            for (int i=0; i<10000000; i++) {
                s.add(i);
            }
            int[] sss = new int[10000000];
            for (int i=0; i<10000000; i++) {
                sss[i] = i;
            }
            BitSet ss = new BitSet(10000000);
            print("ArrayList cost memory: " + RamUsageEstimator.sizeOf(s) + "bytes.");
            print("BitSet cost memory: " + RamUsageEstimator.sizeOf(ss) + "bytes.");
            print("List cost memory: " + RamUsageEstimator.sizeOf(sss) + "bytes.");
            long endAt = System.currentTimeMillis();
            print("Program cost time: " + (float)(endAt-startAt)/1000 + 's');
        }
    }

运行结果为：  
![img](https://ws1.sinaimg.cn/large/0073xHwmgy1fxee24n7scj30nu0d4wg7.jpg)  
可以看到，不同的存储结构所占的内存差别真的是天差地别。  
数组很明显，10<sup>7个int</sup>，再加上引用本身，所占内存不到4M；  
MyBitSet表现很好，只占用了1.25M；  
ArrayList是最恐怖的，竟然占了205M，惊了！  


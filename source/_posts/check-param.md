---
title: 说一下Python项目中的验参
date: 2018.08.19 17:47:00
tags:
- python
- 微服务
---

在积累了一定的工作与项目实战经验后，越来越意识到验参的重要性。
前几天又重读[总结了一下【程序员修炼之道】](https://guerbai.github.io/2018/08/12/pragmatic-programmer-note/)，书中提到，卓有成效的程序员从不相信任何人，包括自己。
关于这句话的一个很重要的实践即是在自己编写的程序中，做好验参工作，使对字段的限制与文档一致。这点可以显著得增强系统的稳定性，保护系统的健壮与数据的一致。

<!--more-->

在实际工作中，发现验参环节并不是那么容易做好，微服务系统有多层结构，每个服务内代码的组织又是分层的， 在哪些场景与环节进行验参比较实用是自己需要考虑清楚的点。
这篇总结一下工作中见到的各Python项目对于验参的各种处理，以及常用的验参的库。

## 需要验参的几个场景
假设项目为一个简单的两层结构，gateway接受浏览器http请求，通过thrift rpc协议调下层service，service将数据写到DB中。

这样一个简单的调用链可以抽出几处需要验参的地方：

- 收到http请求时，对前端传来的参数进行验证，确保前端传来的参数与前端文档中约定的一致；
- service服务代码分层为handler, service, model三层，handler接受到thrift请求，将thrift request对象序列化为dict后，调用service层代码前，需要进行参数验证(包括一些业务上的验参)，确保client端传来的参数与idl中定义的参数规则一致；
- service服务的service层往DB写数据前(包括新增与更新时)需要验参，确保写到数据库中的数据与model文件(orm定义)中定义的规则一致。


## 验参如何做

### if else直接干
之前在写一个Java项目的时候，问到组内的一个较有经验的Java开发在Java中验参通常怎么做，怎样是比较地道的写法。
他开玩笑说，if else不就好了嘛。(当然，之后还是告诉了我可以用javax.validation中的注解很自然轻易地完成这个任务)

诚然，if else可以撸出一切。而且的确我也在一些项目中包括刚参加工作时的小公司的代码里见到过这样的做法，不用引入第三方库，直接进行判断，某字段是否存在，某字段是否为None，字段长度是否超长等。
这的确可以完成工作，但真的不够clean，每次在函数的前部分都要处理这些东西，代码写出来很丑。若要把这种if抽出来，粒度又太细，同时又要使用比如装饰器这种技术将它和函数本体编织起来，而且不同函数要验证的条件往往又是不一样的，之前写的验证方法可能还要再改以达到通用，这就又要再改引用了这个验证方法的方法，等等情况会出现很多问题，所以并不是一个长久的组织方法。

下面介绍几个我见过的用于验参的第三方包，可接避免上面那样的重复造轮子。

### [marshmallow](https://marshmallow.readthedocs.io/en/3.0/)
marshmallow本身是Python中的一个出色的用于做序列化的库，同时也提供了在验参功能。
它允许开发者定义一些schema，schema中可以以各种方式(allow_none, required, lambda)来表述一个字段的规则，同时在反序列化(将外部参数转化为领域对象)时，会自动进行验参工作，并将不符合规则的参数统一组织起来，而且允许开发者自己提供个性化的相应报错信息。

上面说到反序列化，那这位又问了，序列化时它不做验参吗？的确如此，marshmallow的作者认为，序列化是指将自己系统内的数据给提供出去(相当于to_json())，对于它们的质量与来源是我们可以保证的，故不需要在这个时候进行反序列化。
但实际情况也并不往往如此，比如我最近接触到的项目，由于之前没有做好验参工作，且表结构较复杂，会有一些存在库中的历史数据其实是少字段的或者是不符合规则的，在这种情况下，可以先将数据取出来，进行序列化生成dict对象，再用dict对象来调用schema.validate(dict)来专门进行验证，从而搜集信息，修补数据。

它的schema可以按照如下方式定义：
```Python
from marshmallow import Schema, fields, validate, validates

class UserSchema(Schema):
    name = fields.Str(required=True, validate=lambda n: n)
    age = fields.Decimal(required=True, validate=lambda n: n > 18)
    location = fields.Str(required=True)

    @validates('location')
    def validate_location(self, value):
        valid_locations = [u'SHANGHAI', u'TOKYO', u'NEWYORK']
        if value not in valid_locations:
            raise ValidationError('Unknown location.')
```
<div align=center>
![](http://45.76.195.123/images/2019/06/03/1.jpg)

使用marshmallow进行验参
</div>


此外，marshmallow还提供了一些常见规则的验证，比如Email，URL来验证字段是否符合规则，不用再去硬写一些让人头疼的正则。它们都继承于Validator类，你也可以继承它来[编写自己的验证规则类](https://marshmallow.readthedocs.io/en/latest/_modules/marshmallow/validate.html)来扩展marshmallow的能力，使得一切都很地道、好用。

### [webargs](https://github.com/sloria/webargs)
在gateway层面，面对http请求，可以使用webargs包来进行参数提取与校验。
我们知道，http请求传参有多种可能，比如在url中的`?key=value&key2=value2`这种格式，此外，post方法传参的可能就更多了，有plan text，application/json等。

而webargs包便是用来简化这一拿参验参的过程，它让开发者可以通过定义一个schema或是dict的结构来表示自己期望从http中得到哪些参数，以及使用哪些规则。查一下源码的话，很容易发现，它内部也是使用了marshmallow，调用了marshmallow的load函数，最后返回一个dict。
这种方式使用起来对开发还是很友好的，举例如下(抄自项目readme)：
```Python
from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

app = Flask(__name__)

hello_args = {"name": fields.Str(required=True)}
# or use schema
# HelloArgs(Schema):
#     name = fields.Str(required=True)


@app.route("/")
@use_args(hello_args)
# 对应上面
# @use_args(HelloArgs(strict=True))
def index(args):
    return "Hello " + args["name"]


if __name__ == "__main__":
    app.run()

# curl http://localhost:5000/\?name\='World'
# Hello World
```
### [schema](https://github.com/keleshev/schema)
说了上面，哪位又问了，marshmallow与webargs所做的验参都不够专一，前者是为序列化服务，后者更多地是为取参同时进行，有些情况下只有两个参数，不想去定义那些schema，感觉好麻烦，而且只想用单一的验参功能，要怎么做呢？

那么schema就是你想要的。`Schema validation just got Pythonic`
它的用法与api比较pythonic，很语义化而且够函数式，写起来还是比较好玩的，不过要注意正确性。
在工作中我见过一些同事拿它在service中的handler代码层验参。
抄袭项目readme示例代码如下，诸位可以感受下，还是蛮有意思的：

<div align=center>
![](http://45.76.195.123/images/2019/06/03/2.jpg)

schema示例代码
</div>

---
一定不要小看验参这件事，在大型项目的开发中，可能有很多历史遗留问题，兼容性问题，甚至是来自脚本的恶意请求等。你根本无法确定你编写的代码会被怎样调用，如果这些环节失去了这些保障，线上的复杂情况，会让你的代码在一些匪夷所思的地方报出经典的`NoneType` error，甚至有些数据库的字段会被莫名其妙地被写为空，却根本不知道它是在何处发生的。这些错误的发生会让开发人员不知所措，措手不及，因为明明在测试时根本没出现过，极度难以调试。
等到时候再要加校验，已经很困难了。

在经历了一些莫明其妙的问题后，我不得不开始重视验参环节，毕竟没吃过亏还是不知道疼。
我认为验参环节是一种运行时的assert技术，marshmallow与webargs提供的序列化、取参数的同时进行验参我认为是比较好的方案，它不会让开发者在代码中多写一行专门去调验参函数又能把这件事给做得很棒。

做好参数验证，是一次请求，一个函数运行，一次持久化成功的第一道保障，client环境太复杂，我们这些写service的还是要保护好自己啊！
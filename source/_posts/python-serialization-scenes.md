---
title: 谈下python微服务中的序列化场景
date: 2018.08.19 22:34:00
tags:
- python
- 微服务
---

在[上一篇文章](https://guerbai.github.io/2018/08/19/check-param/)中说到了验参，现在接着说另一个微服务中的工程性问题，序列化。
作为编写业务的程序员，常被戏称为CRUD程序员，会增删改查，给个if else给个for就能混碗饭吃。此话倒不假。
在微服务体系下，工作中有时会接触多个项目，各个service与各个gateway，由于维护人员的不同，虽然都是做CRUD的工作，但项目结构与写法却不尽相同。

<!--more-->

这让我回想起刚参加工作时加入一家很小的创业公司，一个简单的单体应用，只有一层，flask的http request进来直接去操作DB，操作sqlalchemy的session，没有任何的抽象，可以说没有任何可以复用的业务代码，每个函数进来都是全新的世界，要开始重新探索，极其丑陋。（甚至可以开玩笑地说，这样有了bug可以将bug只控制在那一个函数以内，不会存在迁一发而动全身的风险。。。）

所以我觉得，将Python微服务中的常见业务代码做到规范化并且尽可能的优雅其实是并不容易的，Python灵活归灵活，但太灵活却容易写出太飘的代码，无法与Java的工程性相提并论。

代码结构层面其实也不用多说，上篇文章中提到过，handler，service，model三层结构，handler进行验参后调service，service可以调service和model，model不可以互相调，验参也是一个比较重要的环节。
这篇来说一下序列化问题，总结一下一个最简单的由前端发起的http请求到gateway再由thrift rpc到service再到db总共要经历多少次序列化和反序列化，以及对Python序列化库marshmallow的应用实践，搞清楚一个简单的CRUD的请求中间到底经过了多少层的转换以及每一次的转换是为了什么。

---
其实就序列化这个描述本身而言，并没有说清楚从哪种类型到哪种类型是序列化，从而在各种场景下都会用到这个词，常常会让人感到混淆。
比如，Python有个pickle库，众所周知是用于将任意Python对象以文件的形式存入磁盘，它有的序列化函数dump是将Python对象转化为写到磁盘上的二进制文件。
json是Python的内置处理json的包，用于序列化json。但这又是什么意思呢？此时的序列化是说将Python的dict类型转化为符合json规范的字符串类型。
而marshmallow的序列化，却是将业务对象转化为Python的dict结构，这就很容易搞乱了，在json的语境来说dict是序列化的输入，而在这里却成了输出。
这就一度搞得我很乱，一度我只能通过dump与记忆来区分各个序列化场景。但不知为什么在某层的某个节点要这样转一下。

在定义不清的时候，去查维基的标准定义往往会很有用。
> 序列化（serialization）在计算机科学的资料处理中，是指将数据结构或物件状态转换成可取用格式（例如存成档案，存于缓冲，或经由网络中传送），以留待后续在相同或另一台计算机环境中，能恢复原先状态的过程。

所以，一个序列化过程，并不确定它的输入方与输出方究竟是什么类型，而是要根据情况而定。我的感受是，越接近业务本身，越接近Python语言本身，离序列化的输入方就越近；越与业务无关、与语言无关，更接近某协议本身表示的，离序列化的输出方向就越近。

下面还是上篇文章的简单场景，前端以http调gateway，gateway以thrift rpc调service，来分别看一个在这个请求链路中，对gateway与service来说，分别经历了几次序列化。

## gateway
在gateway中，比如一个flask应用，我总结序列化与反序列化通常有以下几个过程。
1. 由http请求而来的参数转化为Python的dict，使用flask-restful+webargs(其使用了marshmallw)，将gunicorn或是nginx过来的http协议内的数据反序列化为Python的dict结构；
2. gateway要向service发thrift rpc请求，需要将dict结构反序列化为thrift生成的client代码中对应idl中定义的request对象，这里可以抽出一个方法在抽象层面上做同样结构的dict到相应request的序列化，调用方法可能为`request = wrap_struct(user_info_dict, NewUserRequest)`；
3. 在请求发出后，拿到rpc的response，得到的依然是由thrift生成的代码中由idl定义的response对象，此时可能需要一个序列化的方法将thrift的response对象序列化为dict结构，`create_res = dump_struct(createResponse)`；
当然，上面的两步也可以使用marshmallow来做，但在gateway层再写一堆schema用来做这个事情真的是有些冗余了，一个更好的办法是使用更加抽象的方式，在反序列化时给定一个dict与相应的已经由thrift生成的request类来生成相应object，同时，可以直接由thrift response生成相同层级结构的dict。
4. gateway拿到数据后要给前端http的response，这是一层序列化，flask提供了jsonify将dict转化为相应的结构返回，flask-restful更进了一步，直接在resource函数中返回json，它会自动做这层序列化；
在工作中还见到过一些在这一层使用marshmallow，用来做什么呢？设想，当你调用一个service取回一些数据，比如同样是用户的姓名这个字段，在thrift接口中定义为name，调用其他团队的服务，这个不依赖于你，而同时，之前跟前端定的接口中返回用户名为username，相信各位有一定实践经验的同学都有这种字段名转换的经历，在代码中手动处理这种转换真的有些恶心，此时使用marshmallow的dump_to参数来做就会显得比较优雅。
若不是这种复杂的情况，直接使用dump_struct回来的数据直接返回给前端即可。

## service
现在来说一下基础服务层的各个序列化阶段，与gateway还是有着明显的不同的。
1- 拿到thrift过来的请求，使用上面提到的dump_struct将thrift response反序列化为dict，方便进行验参等进一步操作；
2- 在数据库插入记录前，使用marshmallow的load()方法反序列化，检查各个字段是否符合规则，还见到过一种处理是直接在load()之后插入记录，方法是使用@post_load装饰器，在验参成功后，直接在model中插入记录，并返回给load的调用者，使用起来很自然；
```Python
from marshmallow import Schema, fields, validate, validates

class UserSchema(Schema):
    name = fields.Str(required=True, validate=lambda n: n)
    age = fields.Decimal(required=True, validate=lambda n: n > 18)
    location = fields.Str(required=True)
    
    @post_load
    def make_object(self, data):
        from model.user import User
        return User(**data)
```
3- service调model执行查询，对外要先吐出一层json格式的数据，见过一些不够clean的方式是在model的class中定义to_json()方法(其实是返回dict对象)，将model的各个字段填入dict的key与value，大致长下面这个样子：
```Python
def to_json(self):
    return {
        'name': self.name,
        'age': self.age,
        'location': self.location
    }
```
但这个转换用marshmallow来处理明显会更好一些，直接调用`UserSchema().dump(record).data`即可得到dict对象，这个UserSchema与request进来时load的时候是可以复用的，可以减少编写上面那样不怎么样的代码。同时，上面也提到过，可以使用dump_to来进行model与dict字段的转换，很好用；

4- service得到的dict对象返回给handler，handler使用`wrap_struct(result, UserResponse)`来进行反序列化，生成thrift response对象，最终给到thrift去处理。

## 网络通信中的序列化
上面提到的都是往往都是需要开发自己去处理的，但在这个过程中，还有一些显然存在的序列化过程，这里简单提一下。

**uwsgi协议**
正常情况下，python服务都不可能是裸奔的，它前面往往还有一层uwsgi(或gunicorn)与nginx。
uwsgi有它自己的二进制协议，nginx配置后，将http请求序列化为uwsgi协议的传输二进制给到uwsgi服务，uwsgi再将此二进制反序列化为Python对象交给你的flask应用。

**thrift中的序列化**
上面有很多的地方都提到将request对象交给thrift，然后呢？
作为知名的开源rpc框架，它提供了多种序列化机制。支持xml，json等文本协议，亦可使用thrift或是google Protobuf协议，在可读性与性能方面，用户可以自由选择。
拿到request的Python对象后，根据不同的序列化协议生成相应格式，最终还是要交给socket来进行数据传输处理。
再由socket拿出来后进行反序列化为thrift response。

---

上面提到的thrift中很重要的一点(思想)是，thrift的这些处理都是通过idl为基础，使用代码生成器来生成的，开发人员只需要编写idl文件，就可以得到各种语言的直接可以使用的代码。

由上所述，各种转化真的还蛮多的，难免会有各种重复的字段定义等会出现在项目的各处(在http文档中，在idl中，在marshmallow schema中，在db model中)，参考【[程序员修炼之道](https://guerbai.github.io/2018/08/12/pragmatic-programmer-note/)】中的安利，再借鉴thrift的实践构想，我认为在总结清楚这些常见的调用、序列化、验参等规划与比较好的具体实践、代码编写方式后，可以开发一个代码生成器，由一个类似idl的语言，来生成各阶段的本来要由程序员去手动编写的代码，从而大幅提高整体编码效率与代码质量。
这肯定是可以实现的，因为thrift已经实现了它。
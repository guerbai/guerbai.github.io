---
title: "JS异步方案及实例"
updated: 2017-08-30 17:39:00
---

JavaScript的单线程决定了其解决并发问题的异步特性。

最直接的回调写法，会造成难以维护的callback hell，JS的发现一直在追寻着以程序员写起来更容易为目标的异步写法。    
解决方案有好几个，因为多，就会乱。    

这里以一个实例为线索，来探究各写法的异同与思想。


# 实例

写一个函数，读文件file1.txt于字符串str1, 拿到file1之后读文件file2.txt于字符串str2，拿到str1+str2后，传给最终处理函数。

# 回调函数写法

```JavaScript
var fs = require('fs')
var log = console.log.bind(console)

// callback hell
function two_str_callback(callback) {
	fs.readFile('file1.txt', function (err, data) {
	if (err) {
		console.log(err)
	}

	var str1 = data.toString()
	fs.readFile('file2.txt', function (err, data2) {
		if (err) {
			console.log(err)
		}
		var str2 = data2.toString()
		callback(str1+str2)

		})
	})
}


two_str_callback(log)
```

# 事件发布订阅模式

此处使用[eventproxy库](https://github.com/JacksonTian/eventproxy)。

```JavaScript
var fs = require('fs')
var eventproxy = require('eventproxy')
var log = console.log.bind(console)

function two_str_eventproxy(callback) {
	var ep = new eventproxy()
	ep.all('data1_event', 'data2_event', function (data1, data2) {
		callback(data1+data2)
	})
	fs.readFile('file1.txt', function (err, data) {
		if (err) {
			log(err)
		}
		ep.emit('data1_event', data.toString())
	})
	fs.readFile('file2.txt', function (err, data) {
		if (err) {
			log(err)
		}
		ep.emit('data2_event', data.toString())
	})
}

two_str_eventproxy(log)
```

可以看到，这种写法避免了fs里再套一层fs，阻止了代码横向发展。    
但此种写法代码运行是跳跃的，emit 'data2_event'后，控制会调回ep.all()处。在维护与调试上仍有一些难度。

# Promise

```JavaScript
var fs = require('fs')
var log = console.log.bind(console)
var Promise = require('bluebird')

function two_str_promise(callback) {
	var err_log = function (value) {
		log('err_log:')
		return console.log.bind(console)(value)
	}
	var concat_str = new Promise(function (resolve, reject) {
		fs.readFile('file1.txt', function (err, data) {
			if (err) {
				reject('err happen in file1');
			} else {
				resolve(data.toString())
			}
		})
	})
	concat_str.then(function (value) {
		return new Promise(function (resolve, reject) {
			fs.readFile('file2.txt', function (err, data) {
				if (err) {
					reject('err happen in file2')
				} else {
					resolve(value+data.toString())
				}
			})
		})
	}).then(log).catch(err_log)
}

two_str_promise(log)
```
使用Promise写法，代码是根据正常思维向下发展，并且没有引入像eventproxy那样的跳跃代码。    
缺点也很明显，这么写感觉上实在是太麻烦了。

# async库

处理并发，特别是要进行相同处理的并发，可以使用[async库](https://github.com/caolan/async)。    
注意，这里的async与下面将要提到的async语法糖所指并不是一个东西。

```JavaScript
var async_lib = require('async')

function two_str_async_lib(callback) {
	async_lib.waterfall(
		[
			function (done) {
				fs.readFile('file1.txt', function (err, data) {
					if (err) {
						log(err)
					} else {
						done(null, data.toString())
					}
				})
			},
			function (result, done) {
				fs.readFile('file2.txt', function (err, data) {
					if (err) {
						log(err)
					} else {
						done(null, result+data.toString())
					}
				})
			}
		], function (err, result) {
			if (err) {
				log(err)
			} else {
				callback(result)
			}
		}
	)
}

two_str_async_lib(log)

```
这种写法嘛~，就比较写意了，api的名字也很有趣儿。    
该库还提供了很多处理各种异步情景的api。


# generator

```JavaScript
var fs = require('fs')
var log = console.log.bind(console)

function readfile(file_name) {
	fs.readFile(file_name, function (err, data) {
		it.next(data.toString())
	})
}


function* two_str_generator (callback) {
	var str1 = yield readfile('file1.txt')
	var str2 = yield readfile('file2.txt')
	callback(str1+str2)
}


var it = two_str_generator(log)

it.next()
```
使用generator的写法的意义在于two_str_generator函数中可以用**同步的思路**清楚地表达思路，即先拿str1, 再拿str2，之后加和这样一个逻辑。

关键点在于readfile函数中直接调用it，函数作用域及变量提升的关系，在它被调用时，它知道it是一个generator。传入读到的数据后传给next作为参数即可被str1,str2得到。

缺点是two_str_generator的调用者，被分散开来，一个在从上往下的最外层发起，另一个则是处于readfile这么一个函数中。

为了解决这个执行器调度的问题，tj写了[co](https://github.com/tj/co)模块来提供了一个方案。


# async/await

该写法就是generator的语法糖。除此之外，还对其进行了一些规范与改进。
```JavaScript
var fs = require('fs')
var log = console.log.bind(console)
var Promise = require('bluebird')

function readfile_new(file_name) {
	return new Promise(function (resolve, reject) {
		fs.readFile(file_name, function (err, data) {
			if (err) {
				log(err)
			} else {
				resolve(data.toString())
			}
		})
	})
}

var two_str_async = async function (callback) {
	var str1 = await readfile_new('file1.txt')
	var str2 = await readfile_new('file2.txt')
	callback(str1+str2)
}

two_str_async(log)
```

可以看到，与上一个例子相比，不需要使用next调用，亦没有使用co模块，其内置了执行器。    
将await的函数返回一个promise对象，其便可自动执行。    
此时的await相当于promise的then操作，在这个层面上，async/await又是promise的语法糖。
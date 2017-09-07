---
title: "项目中有关HTTP的几个细节"
updated: 2017-04-04 16:00:00
---

# 首部与HTTP认证

需要此认证时，会跳出窗口，保护窗口由Web浏览器提供。

首部准确地控制着如何在Web浏览器和Web服务器之间来回传递信息，以及传递何种信息。

HTTP认证的基本思想是，服务器会"扣留"一个受保护的Web页面，然后要求浏览器向用户询问一个用户名和口令。若输入正确，则浏览器会继续发送页面。

而浏览器和服务器之间的这个对话正是通过首部完成的，首部是一个短小的文本消息，包含所请求或传送的特定指令。

```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="some word"
```

本拟使用Flask-HTTPAuth库来实现此点。    
后发现浏览器自带弹窗与该库返回的401statusCode均不符合需求。    


# Cookie与Session.

## Cookie

cookie允许将小段数据持久地存储在**客户端**，类似于变量，key, value。cookie可以有一个到期时间，到达时这个cookie就会被销毁。    
若创建cookie时未指定时间，则其会在浏览器关闭时被销毁。    

使用cookie来解决登陆问题便不需要去使用HTTP认证。    
HTTP认证对于限制访问单个页面很方便，但是没有提供一种好方法允许用户结束页面访问时完成“注销”。

而使用cookie意味着允许用户注销，删除其cookie即可。删除cookie的方法为将其到期时间设置为一个已经过去的任意一个时间。

## session

session与cookie类似，不过其将数据存储在**服务器**，更为安全。

会话结束则session会消失，而会话往往会在关闭浏览器时结束。


## solution: session+cookie

用户登陆，同时设置session和cookie，关闭浏览器时，注销当前session，而cookie保留。    
下一次打开网页时，利用cookie重新创建session。    
如是工作直到cookie到期。

# 跨域问题及解决方案

同源政策的目的，是为了保证用户信息的安全，防止恶意的网站窃取数据。

具体有三点：
1. 协议相同
2. 域名相同
3. 端口相同

非同源会受到以下三种限制：
1. Cookie、LocalStorage 和 IndexDB 无法读取。    
2. DOM 无法获得。(如果两个网页不同源，就无法拿到对方的DOM。典型的例子是iframe窗口和window.open方法打开的窗口，它们与父窗口无法通信)    
3. AJAX 请求不能发送。

服务器也可以在设置Cookie的时候，指定Cookie的所属域名为一级域名，比如.example.com。    
详见flask set_cookie()接受参数。 

CORS为'跨域资源共享'。需要浏览器和服务器同时支持，克服了AJAX受同源政策的限制。    
浏览器端，是浏览器自动处理，代码完全一样均为XMLHttpRequest。

浏览嚣会在头信息之中，增加一个Origin字段。    
上面的头信息中，Origin字段用来说明，本次请求来自哪个源（协议 + 域名 + 端口）。服务器根据这个值，决定是否同意这次请求。    
浏览器会根据服务器返回(或者不返回)Access-Control-Allow-Origin来判断这次请求是否出错。

对于非简单请求，比如Content-Type字段的类型是application/json。会在正式通信之前，增加一次HTTP查询请求，称为"预检"请求(preflight)。

Access-Control-Allow-Origin字段是每次回应都必定包含的。

Flask-cors
```Python
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/v1/users")
def list_users():
    return "user example"
```

`@cross_origin()`可作用于单个路由.

CORS with cookies: `CORS(app, supports_credentials=True)`

## CORS与CSRF    

CSRF为跨站请求伪造。    
A网站(骇客网站)，B网站(天线宝宝网站)。    
CORS发起的跨域请求，并非完全阻止，而是跨域请求可以正常发起，但返回的响应会被浏览器拦截。    
CORS 机制的目的是为了解决脚本的跨域资源请求问题，不是为了防止 CSRF。    
在同源策略的限制下，响应会被拦截，即阻止获取响应，但是请求还是发送到了后端服务器。    
因为Access-Control-Allow-Origin响应头是由浏览器来解析的，即使我们设置了正确的 CORS 规则，请求仍已经发起了，所以是无法防止 CSRF。

关于跨域与cookie:    
服务器会通过Access-Control-Allow-Credentials来告诉浏览器是否发送cookie。    
Access-Control-Allow-Credentials:true并不是让请求携带A站点的cookie发送到B站点服务器，其实是让请求携带B站点的cookie发送到B站点服务器。    
到了这里，便有一个迷惑的点，即A网站，往B网站，发请求，若服务器不同意，为何可以携带B网站的cookie. 这与同源政策相悖。

原因大抵是这样：    
如果B站点的响应头里有Access-Control-Allow-Origin: * | http://www.a.com，那么跨域请求会成功，但是该请求不会携带B站点所在域的cookie。    
**如果该请求不是ajax请求，而是img、script、iframe标签等发起的请求，那么该请求会携带B站点所在域的cookie，跟没跨域直接访问B站点对应的资源一样。**    
故CORS防不了CSRF。

*参考资料*：
1. [Head First PHP&MySQL](https://book.douban.com/subject/6011680/)
2. [浏览器同源政策及其规避方法](http://www.ruanyifeng.com/blog/2016/04/same-origin-policy.html)
3. [跨域资源共享 CORS 详解](http://www.ruanyifeng.com/blog/2016/04/cors.html)
4. [Flask-CORS Document](http://flask-cors.corydolphin.com/en/latest/index.html)
5. [跨域ajax请求如何携带cookie](http://www.qdfuns.com/notes/17631/a55691705874e631c5121fa26fea86d5.html)

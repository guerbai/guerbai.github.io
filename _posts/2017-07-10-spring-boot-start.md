---
title: "Spring Boot起步"
updated: 2017-07-10 15:30:56
---

# Spring Boot是什么
Spring Boot是一套全新的框架，其提供了一种全新的编程范式，使得开发人员不用在Spring的配置中耗费过多的时间，能够更加专注于应用程序的功能，从而在最小的阻力下开发Spring应用程序。

从本质上来说，Spring Boot就是Spring，它使用了特定的方式来配置Spring应用，做了那些没有开发人员自己也会去做的Spring Bean配置。有了它，便不用再写这些样板配置了，可以专注于应用程序的逻辑， 那些属于应用程序独一无二的东西。

Spring Boot非常适合于当今蓬勃发展的快速应用开发领域及微服务架构。

# Spring Boot不是什么
## 不是应用服务器
误解点来自其可以把Web应用程序变为可自执行的JAR文件，不用部署到传统Java应用服务器里就能在命令行里运行。    
这是由于Spring Boot在应用程序中内嵌了一个Servlet容器(Tomcat、Jetty或Undertow)，然而能跑起来是其内嵌容器实现的，而不是Spring Boot本身。

## 没有任何形式的代码生成
它利用了Spring 4的条件化配置特性，以及Maven和Gradle提供的传递依赖解析，以此实现Spring应用程序上下文里的自动配置。

# 主要特性
+ 自动配置
+ 起步依赖
+ 命令行界面
+ Actuator

# 项目初始化
上[Spring Initializr](http://start.spring.io/)网站，输入Group，Artifact及Dependencies后Generate Project生成maven项目，下载过后的压缩包解压后使用Intellij打开。    
在生成的项目中会自动生成项目结构及pom.xml文件，并且根据在Dependencies中的输入在pom.xml中生成要引入的
包，非常方便。

# 注解：
在生成的项目中，项目主文件App.java中内容如下。

```Java
package readinglist;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class App {
public static void main(String[] args) {
    SpringApplication.run(App.class, args);
    }
}
```
注意到注解为@SpringBootApplication。    
其等价于@Configuration，@ComponentScan与@EnableAutoConfiguration的和。    

## @Configuration注解
标明该类使用Spring基于Java的配置。    
Spring中提供了两种方式(xml与java)的方式来进行配置bean。
该注解标明了该类使用后一种方式来进行配置。

## @ComponentScan注解
表示启动组件扫描，这样写的web控制器类和其他组件才会被扫描到从而注册入整个Spring的服务。

## EnableAutoConfiguration注解
该注解属于Spring Boot，它开启了自动配置开关。

## RestController注解
在类上标明此注解表明该类是一个web控制器类，它源于Spring MVC，会被 @ComponentScan扫描到。

## @RequestMapping, @GetMapping, @PostMapping...
这些注解通常位于@RestController类之内的函数上，括号内的路提供相应的服务。在使用@RequestMapping时，需要参数来指定请求方式，@GetMapping等为两者的简写。
当类上亦有@RequestMapping时，则路径为类上路径与函数上路径相加。

## @Autowired注解
Spring框架中，使用xml配置了一个Bean，当该Bean被注入到某类作为属性时，在聚合它的类里，建议将其定义成私有的域变量，并且要配套写上get和set方法。
而该注解可以让Spring自动设置该属性的set/get方法。

# 自动配置
在Spring Boot出现之前，即使只是想用Spring写一个简单的Hello World，那也是要进行不少的配置。    
Spring Boot则提供了自动配置的机制，来替开发人员进行这些操作。    
在之前从Spring Initializr中搞下来的模板便可直接运行，并且很重要的是，一行配置也不用写。    
据说Spring Boot根据各种情况以及细节比如classpath中的jar包等信息，利用Spring的条件化配置，在启动项目时替你进行了200个左右的决定，来让程序跑起来。

# 自定义配置
自动配置当然是好的，但在某些情况下，它做的决定并不是你想要的，好消息是Spring Boot并不是完全对开发人员隐藏这一切。    
首先，在spring-boot-starter-actuator中提供了机制来查看所有它替你做的决定是什么。    
在发现了想要修改的点之后，还可以进行修改。    
想要覆盖它的自动配置，所要做的仅仅是编写一个显示的配置。

这种修改的灵活性也非常地高，像传统的xml，Java Bean(利用@Configuration注解)，甚至groovy都可以进行配置，亦可以在application.properties中以key-value的形式在更细的粒度上对配置进行控制。


# application.properties
常至于src/main/resources/文件夹下。    
此为Spring Boot的配置文件，与Spring的大段XML不同，它可以越过@Bean这一层直接去更改某个点的配置，从而可以使开发人员人更细粒度上对Spring Boot进行微调。    
而它本身是被Spring Boot自动加载的。    
以下是一些可能会用到的配置项。    
同时，除了在日志的专门配置文件中配置logger属性，亦可以此文件内对日志模式进行微调。

+ 以不同端口启项目：`application.properties中server.port=8000`
+ 配置数据源`spring.datasource.url=jdbc:mysql://localhost:3306/test?characterEncoding=UTF-8`

# 起步依赖
Spring Boot的依赖管理不会像其他Java项目那样受到各依赖版本不兼容而带来的困扰。它通过功能将各个经过充分测试的依赖打包为它的起步依赖。    
比如要创建一个web程序，则引入spring-boot-starter-web依赖之后，相关的几个包如Spring MVC及Jackson早已自动存在于该starter中。不用关心依赖的细节。

在前文所说的Spring Initializr中，只需要在dependencies中选一个web即可。

同时，Maven构建说明中将spring-boot-starter-parent作为上一级， 只需要指定parent的版本号，下面其他关于Spring Boot的starter都不再需要指定版本号。

总结一下，起步依赖的好处在于，使得开发人员能够在项目依赖的层面**只关心功能**，而**不需要知道依赖到底是什么**，而且**不再需要考虑版本兼容问题**。

# profile
profile区分不同环境(local, test, online)。    
在有以上三个环境的情况下，在application.properties平级建立application-local.properties、application-test.properties、application-online.properties。
将在各环境不同的配置比如数据源信息分别写在各自环境的配置文件下。    
同时，在application.properties(主配置文件)中，添加字段如下:
`spring.profiles.active=local`

在项目打包时，必定会读取主配置文件，在读到了此配置项后，便会去读取local环境的配置文件。从而达到区分环境的目的。    
使用该方法在打包之前**一定要记得去修改主配置文件的该配置项**，另外还有使用maven进行大段配置并在打包时加-P参数的方法，但较此法感觉更为麻烦，暂不深究。

在此三配置文件存在的情况下，各配置文件中各有一个自定义的key为'weekday'，值分别为'Monday'(local)，'Tuesday'(test)，'Friday'(online)。    
在源码的类中，可以使用这种方法得到不同环境下该key的正确值。

```Java
public class App {
    @Value("${weekday}")
    private String weekday;
}
```

此外@Profile("online")亦可作为注解作用于类或方法上，使得同一方法在不同环境采取不同的实现，或者在不同环境采取不同的Java配置。

# 测试
SpringJUnit4ClassRunner是Spring提供的一个JUnit类运行器，会为JUnit测试加载Spring应用程序上下文。    
对于Spring Boot程序而言，加上@SpringApplicationConfiguration(classes=App.class)的注解可加载所有的Spring Boot做的自动配置。    
由Spring Initializr生成的项目骨架中有一个示例测试类。

## 对源码中类的测试
在测试类的@Test下的测试方法中可以测试该类提供的各种功能。    
在测试类中可通过@Autowired注入源码中编写的类，并对其功能进行测试。

## 测试rest服务
要测试一个@RequestMapping注解下的函数，需要投入一些实际的http请求，此处有Spring Mock MVC包可用。    
它能在一个近似真实的模拟Servlet容器里测试控制器，而不用实际启动应用服务器。    
该点暂时可由python request脚本或postman

# Actuator
引入spring-boot-starter-actuator起步依赖后便可以使用其提供的功能来监测程序的内部细节信息及运行情况。    
其提供了一些rest风格的web服务，可以通过浏览器打开，获得信息。

+ 获取Bean装配报告: "/beans"，可以看到程序都装配了哪些Bean，以及其相关信息;
+ 程序运行时的自动配置: "/autoconfig"，可以看到为何会产生以上的Bean;
+ 查看配置属性: "/env"，包括application.properties中的key-value;
+ 程序所有路由与方法的映射记录: "/mappings";
+ 查看程序健康信息: "/health"。

还有一些更详细更细节的信息路由，以及对这些路由访问权限的控制，具体可见官方文档。

# 提供Rest服务
通过@RestController注解于类以及@RequestMappings注解于类方法并返回Map<String, Object>类型的值便可提供Rest服务。

## 接收参数
常用的有@PathVariable与@RequestParam及@RequestBody。    
@PathVariable为url中对'/users/{username}'风格参数的解析;    
@RequestParam为url中?后key-value的解析；    
@RequestBody用于解析post请求中的json，即通常使用的python发post请求的参数可用其得到。    
举例：
```
@PostMapping("/info")
public Map<String, Object> getInfo(@RequestBody Map<String, Object> params) {
    params.put("key", "value");
    return params;
}
```
以上就是一个完整的可用于post的获取json返回的请求。

## rest风格url设计：

> 当URL指向的是某一具体业务资源（或者资源列表），例如博客、用户时，使用@PathVariable
> 当URL需要对资源或者资源列表进行过滤、筛选时，用@RequestParam

## ServletInitializer
要提供web Rest服务，仅将项目打包为war是不够的，没有web.xml或Servlet初始化类容器无法识别。    
对此，Spring Boot的做法是让App继承SpringBootServletInitializer，覆盖configure()方法来指定Spring配置类，帮助容器初始化。    
代码为:

```Java
public class App extends SpringBootServletInitializer {
    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder builder) {
        return builder.sources(Application.class);
    }
}
```

## 处理异常
在控制器类中，@ExceptionHandler注解于方法上可处理异常，并进行相应处理并返回。    
控制器类上使用@Controller时这样的方法作用于此类，使用@ControllerAdvice时则作用于Spring应用全局。    
示例：
```
@ExceptionHandler({Exception.class})
public String handleError(HttpServletRequest req, MyException e) {
    return "ErrorOccur";
}
```

# 取得SpringBoot上下文
A类中使用@autowired或@Value注入属性，在别处new A()时会报NullPointerException。原因是没有获得SpringBoot的上下文。解决方法如下：

```Java
@Component
public class ApplicationContextHolder implements ApplicationContextAware {
    private static ApplicationContext applicationContext;

    @Override
    public void setApplicationContext(ApplicationContext ctx) throws BeansException {
        applicationContext = ctx;
    }

    /**
     * Get application context from everywhere
     *
     * @return
     */
    public static ApplicationContext getApplicationContext() {
        return applicationContext;
    }

    /**
     * Get bean by class
     *
     * @param clazz
     * @param <T>
     * @return
     */
    public static <T> T getBean(Class<T> clazz) {
        return applicationContext.getBean(clazz);
    }

    /**
     * Get bean by class name
     *
     * @param name
     * @param <T>
     * @return
     */
    @SuppressWarnings("unchecked")
    public static <T> T getBean(String name) {
        return (T) applicationContext.getBean(name);
    }
}
```
一个A类的例子：
```Java
public class RedisUtils {
    private static RedisTemplate redisTemplate;
    
    private static RedisTemplate getRedisTemplate() {
        if (redisTemplate == null) {
            redisTemplate = AppCtxHolder.getBean('redisTemplate');
        }
        return redisTemplate;
    }
}
```

# maven
使用插件运行程序: mvn spring-boot:run。

打war包：
```xml
<packaging>war</packaging>
```
打包时指定名称:
```
<build>
    <finalName>finalName</finalName>
</build>
```

  [1]: start.spring.io
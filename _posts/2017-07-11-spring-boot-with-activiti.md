---
title: "Spring Boot与Activiti集成"
updated: 2017-07-10 16:10:32
---

# Activiti Java API
## 引入起步依赖
项目pom.xml中加入：
```xml
<dependency>
    <groupId>org.activiti</groupId>
    <artifactId>activiti-spring-boot-starter-basic</artifactId>
    <version>${activiti.version}</version>
</dependency>
```

## 注意点
一定要注意，**在src/resources/processes文件夹下要有bpmn流程文件**。    
Spring Boot在项目启动时会自动加载这些流程文件并部署，如找不到会报错。    
可以在其中画一个start.bpmn，只有开始与结束。    

**更新**    
改变配置项可使得spring boot不扫描processes文件夹。    
方式为在application.properties中添加如下配置：    
`spring.activiti.check-process-definitions=false`    

## 引入数据库连接依赖
```xml
<dependency>
	<groupId>com.h2database</groupId>
	<artifactId>h2</artifactId>
	<version>1.4.183</version>
</dependency>
```
此处引入h2。    
h2是内存数据库，生命周期即为项目的一次启动时间。在测试时，比如测某个流程文件的正确性时很有用。    
此时项目便已经引入了Activiti，可直接启动，由于classpath中有h2包，聪明的Spring Boot会自动使用h2数据库作为引擎的配置。

## 在项目中使用Activiti Java API
此时便可在项目源码中使用全套的Activiti API。
```Java
@Configuration
@ComponentScan
@EnableAutoConfiguration
@RestController
public class MyApplication {

    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
    
    @GetMapping("/definition-count")
    public Map<String, Object> getEngineInfo() {
        Map<String, Object> res = new HashMap<String, Object>();
        ProcessEngine engine = ProcessEngines.getDefaultProcessEngine();
        RepositoryService repositoryService = engine.getRepositoryService();
        long count = repositoryService.createProcessDefinitionQuery().count();
        res.put("count", count);
}
```
之后点击Intellij的运行按钮，便可启动项目。    
代码中已经写了一个rest api，其中使用了Activiti API，查询了definition的数目。    
之前在processes中提供了start.bpmn，启动时已自动部署。    
此时curl此API，便可得到结果：
```Json
{
    "count": 1
}
```


# Activiti Rest API

## 引入activiti rest api
Activiti本身提供了一套Rest API，可以很方便得集成到自己的项目中，提供对外服务。    
引入方法为在pom.xml中加入activiti-spring-boot-starter-rest-api即可。    
```xml
<dependency>
	<groupId>org.activiti</groupId>
	<artifactId>activiti-spring-boot-starter-rest-api</artifactId>
	<version>${activiti.version}</version>
</dependency>
```
此时，运行Spring Boot项目，在启动项目的log中即可看到rest-api已为该项目提供了很多的REST路由，比如"/repository/process-definitions"，此时访问该路由会得到401认证错误，而不是404，说明activiti rest api已起了作用。    

## 关闭身份认证
将该项目做为整个项目的逻辑引擎，身份认证权限等问题已在其他模块进行了处理，在此处并不希望受到401的制约。    
解决方法以是使用@SpringBootApplication时，排除自动配置几个类。    
```Java
@SpringBootApplication(exclude={
    org.springframework.boot.autoconfigure.security.SecurityAutoConfiguration.class,
    org.activiti.spring.boot.SecurityAutoConfiguration.class,
    org.springframework.boot.actuate.autoconfigure.ManagementWebSecurityAutoConfiguration.class,
})
```
如是，再启动项目，便可通过curl访问"localhost:8080/repository/process-definitions"，得到在项目启动时自动部署的start.bpmn的信息。

# 配置ProcessEngine使用MySQL
之前并没有对数据源进行配置，只是引入了h2依赖，项目启动时，自动配置使用了该数据库，但并不适用于生产环境。
## 引入依赖
配置其连接MySQL首先要引入两个依赖。
```xml
<dependency>
	<groupId>mysql</groupId>
	<artifactId>mysql-connector-java</artifactId>
	<version>6.0.6</version>
</dependency>
<dependency>
	<groupId>org.apache.tomcat</groupId>
	<artifactId>tomcat-jdbc</artifactId>
	<version>8.0.15</version>
</dependency>
```
## 配置连接项
之后在各profile的application.properties下配置数据库连接选项：
```Java
spring.datasource.url=jdbc:mysql://localhost:3306/activiti?characterEncoding=UTF-8&Reconnect=true
spring.datasource.username=root
spring.datasource.password=rootpwd
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
```
做了如上操作之后，会同时影响到activiti java api以及rest api的引擎配置。    
控制spring.profiles.active项便可做到**区分不同环境的数据库连接**。

**注**： 而使用spring.datasource.url方式配置，对Spring Boot而言属于jdbc连接，同时对于Activiti而言，基于jdbc参数配置的数据库连接会使用默认的MyBatis连接池。

# 单例模式获取流程引擎实例
在上述修改后，可在代码内由`ProcessEngines.getDefaultProcessEngine();`即可获取连接mysql的引擎。    
整个项目内有一个引擎实例即可，避免造成混乱以及不必要的性能消耗。
方式为写一个util类：
```Java
public class ActivitUtils {

    private static ProcessEngine processEngine;
    
    public static ProcessEngine getProcessEngine() {
        if (processEngine == null) {
            processEngine = ProcessEngines.getDefaultProcessEngine();
        }
        return processEngine;
    }
}
```
这样在其他控制器中，即可轻易地由`ProcessEngine processEngine = ActivitiUtils.getProcessEngine()`获取引擎实例。

# Activiti actuator
Spring Boot学习章节说明了Spring Boot中actuator的作用。    
而activiti则扩展了actuator，在对Spring Boot的监控基础上，提供了关于工作流方面的信息监控。
```xml
<dependency>
	<groupId>org.activiti</groupId>
	<artifactId>activiti-spring-boot-starter-actuator</artifactId>
	<version>${activiti.version}</version>
</dependency>
```
引入此依赖后启动项目，需要关闭权限认证，在application.properties中设置`management.security.enabled=false`。    
此时可通过"http://localhost:8080/activiti"得到关于流程处理的信息，包括部署流程的信息，以及流程今日完成任务等信息。

# 测试流程文件
在src/test/java/package/下，写一AbstractTest.java文件，在该类中实例化Activiti的几个服务对象。
```Java
public abstract class AbstractTest {

    @Rule
    public ActivitiRule activitiRule = new ActivitiRule("activiti.cfg.xml");

    protected ProcessEngine processEngine;
    protected RepositoryService repositoryService;
    protected RuntimeService runtimeService;
    protected TaskService taskService;
    protected HistoryService historyService;
    protected IdentityService identityService;
    protected ManagementService managementService;
    protected FormService formService;

    @BeforeClass
    public static void setUpForClass() throws Exception {
        System.out.println("++++++++ 开始测试 ++++++++");
    }

    @AfterClass
    public static void testOverForClass() throws Exception {
        System.out.println("-------- 结束测试 --------");
    }

    @Before
    public void setUp() throws Exception {
        processEngine = activitiRule.getProcessEngine();
        repositoryService = activitiRule.getRepositoryService();
        runtimeService = activitiRule.getRuntimeService();
        taskService = activitiRule.getTaskService();
        historyService = activitiRule.getHistoryService();
        identityService = activitiRule.getIdentityService();
        managementService = activitiRule.getManagementService();
        formService = activitiRule.getFormService();
    }

}
```
其中用到的activiti配置文件位于scr/test/package/resources/下，内容为：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
		xsi:schemaLocation="http://www.springframework.org/schema/beans
				http://www.springframework.org/schema/beans/spring-beans.xsd">

	<bean id="processEngineConfiguration" class="org.activiti.engine.impl.cfg.StandaloneInMemProcessEngineConfiguration">
		<property name="databaseSchemaUpdate" value="true"/>
		<property name="jobExecutorActivate" value="true" />
		<property name="history" value="full"/>

	</bean>
</beans>
```
其使用了StandaloneInMemProcessEngineConfiguration来实例化引擎，每次测试的数据不会留下痕迹，非常适用于测试流程文件。将流程文件置于src/test/resources/processes文件夹下。    
Activiti在测试开始时提供了部署的api。
```Java
public class easiTest extends AbstractTest {
    @Test
    @Deployment(resources = {"processes/easi.bpmn})
    public void testEasi() {
    }
}
```
如上，在测试方法上套一个`@Deployment(resources={"processes/easi.bpmn"})`，其便能在测试开始时自动将该工作流部署到AbstractTest.java中实例化的processEngine中。

此外，对于流程图中所写的listener，其位置在src/test/下或在src/java/下均可正常运行。
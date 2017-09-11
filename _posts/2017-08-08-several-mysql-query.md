---
title: "几个MySQL查询"
updated: 2017-08-08 13:38:40
---

最近时间在考虑报表的实现，基于用户数、应用场景等各方面因素决定使用原生SQL查询，让MySQL来计算结果的方案。    

过程中，又学习了一波SQL查询语法，特别是对于join与group by。    
感觉自己之前写业务不过只用了潜能的九牛一毛。特记录几个典型查询。

# inner join
查询父节点所有直属子节点。
```sql
select company.name from company
inner join company_link
on (company.uuid=company_link.child)
where company_link.parent=(
    select uuid from company where id=id1
);
```

# 全文索引

创建：

```sql
create fulltext index ft_path on company_link (parent_path);
```

查询：
查询父节点下所有子节点的所有订单。

```sql
select order.id from order
where order.company_id in (
    select company.uuid from company
    inner join company_link
    on (company.uuid=company_link.child)
    where match (company_link.parent_path) against (
        (select uuid from company where id=id1)
    )
);
```

# 取得某个中间结点的所有叶子结点

自联结+左联结:
```sql
select company.name from company
where uuid in (
    select u1.child from company_link u1
    left join company_link u2
    on (u1.child=u2.parent)
    where match (u1.parent_path) against (
        (select uuid from company where uid=uid1)
    ) and u2.parent is null
);
```

# 根据时间分组
```sql
select
count(id), from_unixtime(ctime, '%Y-%m-%d') as day
from company
group by day order by day;
```

# case-when语句
```sql
select count(id),
    case
        when city in ('北京', '上海') then city
        else 'other'
    end
    as cy
from company group by cy;
```

# 函数式sql

这里的感觉是，由内往外传，当需要根据内层表查询字段来进行group by时，便要将其作为该function的输出， 使用inner join on来将该输出作为更外层的输入，可如是一层一层往上传，并在最高层进行group by。

拿上面的全文索引处的例子来举例，要统计order数量，并根据城市来进行group by，中间形成一个临时表。

```sql
select 
count(order.price), cpy_table.city as cti
from order
inner join (
    select company.uuid, company.city from company
    inner join company_link
    on (company.uuid=company_link.child)
    where match (company_link.parent_path) against (
        (select uuid from company where id=id1)
    ) 
) cpy_table
on (order.company_id=cpy_table.uuid)
group by cti;
```

# Json字段

where子句查询：    
`select ctime, cost from order where customize->'$.key1'=val1;`    

增加虚拟列及索引：    
`alter table order add customize_key16 varchar(50) generated always as (customize->'$.key16');`    
`alter table order add index ix_key16_f (customize_key16);`    
增加虚拟列后查询, 注意此处与上面where子句的不同，使用此种方法才能用到索引：    
`select ctime, cost from order where customize_key16='"nihil"';`
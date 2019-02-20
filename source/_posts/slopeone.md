---
title: Slope One进行评分测试
date: 2019.02.20 16:17:35
tags:
- 推荐系统
- 算法
---

Slope One是一种基于物品的协同过滤算法，在2005年的paper《Slope One Predictors for Online Rating-Based Collaborative Filtering》被提出，用于预测用户对某一给定的物品的评分。

依然使用[上一篇](https://guerbai.github.io/2019/02/16/intro-to-collaborative-filtering/)中提到的自己编造的少量[评分数据](https://gist.githubusercontent.com/guerbai/3f4964350678c84d359e3536a08f6d3a/raw/f62f26d9ac24d434b1a0be3b5aec57c8a08e7741/user_book_ratings.txt)来描述该算法的运作机制。    

<!--more-->

首先依然是加载数据和生成用户物品关系矩阵如下。

```python
data_url = 'https://gist.githubusercontent.com/guerbai/3f4964350678c84d359e3536a08f6d3a/raw/f62f26d9ac24d434b1a0be3b5aec57c8a08e7741/user_book_ratings.txt'
df = pd.read_csv(data_url, sep = ',', header = None, names = ['user_id', 'book_id', 'rating'])
user_count = df['user_id'].unique().shape[0]
item_count = df['book_id'].unique().shape[0]
user_id_index_series = pd.Series(range(user_count), index=['user_001', 'user_002', 'user_003', 'user_004', 'user_005', 'user_006'])
item_id_index_series = pd.Series(range(item_count), index=['book_001', 'book_002', 'book_003', 'book_004', 'book_005', 'book_006'])

def construct_user_item_matrix(df):
    user_item_matrix = np.zeros((user_count, book_count), dtype=np.int8)
    for row in df.itertuples():
        user_id = row[1]
        book_id = row[2]
        rating = row[3]
        user_item_matrix[user_id_index_series[user_id], book_id_index_series[book_id]] = rating
    return user_item_matrix

user_item_matrix = construct_user_item_matrix(df)
print (user_item_matrix)
```

    [[4 3 0 0 5 0]
     [5 0 4 0 4 0]
     [4 0 5 3 4 0]
     [0 3 0 0 0 5]
     [0 4 0 0 0 4]
     [0 0 2 4 0 5]]


## 构造物品评分差异矩阵

接下来生成两个shape为`(item_count, item_count)`的矩阵`differential_matrix`与`weight_matrix`。    
前者记录物品两两之间的被评分差异情况，后者记录对某两个物品共同评分的人数，用于之后的计算做加权。

以上面`user_item_matrix`举例来讲，index为2与4的item的共同评分人数为2(index为1与2的用户)，则计算这两者的评分差异为:    
`((4-4)+(5-4))/2 = 0.5`，故在`differential_matrix[2][4]`的位置填上0.5，同时在`weight_matrix[2][4]`的位置填上2。    
同时，反过来，`differential_matrix[4][2]`的值为-0.5，而`weight_matrix[4][2]`的位置依然为2，这种相对应的位置不需要重复计算了。

下面的函数接受一个用户物品关系矩阵，按照上述方法计算出这两个矩阵。


```python
import numpy as np
import pandas as pd


def compute_differential(ratings):
    item_count = ratings.shape[1]
    differential_matrix = np.zeros((item_count, item_count))
    weight_matrix = np.zeros((item_count, item_count))
    for i in range(item_count):
        for j in range(i+1, item_count):
            differential = 0
            i_rating_user_indexes = ratings[:, i].nonzero()[0]
            j_rating_user_indexes = ratings[:, j].nonzero()[0]
            rating_i_j_user = set(i_rating_user_indexes).intersection(set(j_rating_user_indexes))
            user_count = len(rating_i_j_user)
            if user_count == 0:
                continue
            for user_index in rating_i_j_user:
                differential += ratings[user_index][i] - ratings[user_index][j]
            weight_matrix[i][j] = user_count
            weight_matrix[j][i] = user_count
            differential_matrix[i][j] = round(differential/user_count, 2)
            differential_matrix[j][i] = -differential_matrix[i][j]
    return differential_matrix, weight_matrix

differencial_matrix, weight_matrix = compute_differential(user_book_matrix)

print ('differencial_matrix')
print (differencial_matrix)
print ('-----')
print ('weight_matrix')
print (weight_matrix)
```

    differencial_matrix
    [[ 0.   1.   0.   1.   0.   0. ]
     [-1.   0.   0.   0.  -2.  -1. ]
     [-0.   0.   0.   0.   0.5 -3. ]
     [-1.   0.  -0.   0.  -1.  -1. ]
     [-0.   2.  -0.5  1.   0.   0. ]
     [ 0.   1.   3.   1.   0.   0. ]]
    -----
    weight_matrix
    [[ 0.  1.  2.  1.  3.  0.]
     [ 1.  0.  0.  0.  1.  2.]
     [ 2.  0.  0.  2.  2.  1.]
     [ 1.  0.  2.  0.  1.  1.]
     [ 3.  1.  2.  1.  0.  0.]
     [ 0.  2.  1.  1.  0.  0.]]


## 进行评分预测

得到上述两个矩阵后可以根据用户的历史评分，为其进行未发生过评分关联的某物品的评分预测。

比如要为index为1的用户`user_002`预测其对index为3的物品`item_004`的评分，计算过程如下：    
先取出该用户看过的所有书，index分别为`[0, 2, 4]`;    
以index为0的物品`item_001`开始，查`differencial_matrix[3][0]`值为-1，表示`item_004`平均上比`item_001`低1分，以该用户对`item_001`的评分为5为基准，`5+(-1)=4`，则利用`item_001`可对`item_004`做出的评分判断为4分，查`weight_matrix`表知道同时评分过这两个物品的用户只有一个，置信度不够高，使用`4*1=4`，这便是加权的含义；    
但这还没完，再根据index为2、4的item分别做上一步，并将得到的值加和为15，作为分子，分母为每次计算的人数之和，即加权平均，为4；    
最后得此次预测评分为`15/4=3.75`。    

下面的函数接受五个参数，分别为三个矩阵，用户id，物品id，结果为预测值。


```python
def predict(ratings, differencial_matrix, weight_matrix, user_index, item_index):
    if ratings[user_index][item_index] != 0: return ratings[user_index][item_index]
    fenzi = 0
    fenmu = 0
    for rated_item_index in ratings[user_index].nonzero()[0]:
        fenzi += weight_matrix[item_index][rated_item_index] * \
            (differencial_matrix[item_index][rated_item_index] + ratings[user_index][rated_item_index])
        fenmu += weight_matrix[rated_item_index][item_index]
    return round(fenzi/fenmu, 2)
```


```python
predict(user_book_matrix, book_differencial, weight_matrix, 1, 3)
```




    3.75



## 评价

**简单易懂**：参见代码；    
**存储**：存储上除了`user_item_matrix`，还需要存下`differencial_matrix`与`weight_matrix`，为节省空间，可以只存后两者的对角线的右上部分即可；    
**预测时间复杂度**：用户评价过的物品数为x，则做一次预测的时间复杂度为O(x)；    
**更新时间复杂度**：当用户新进行一次评分时，需要更新两矩阵，则`weight_matrix`中只可能是物品已评价过的x个物品中的物品可能会+1，同理在差值矩阵，只需计算出其与x个物品各自的评分差值更新到相应位置即可，无需重新计算两个矩阵，是飞快的，时间复杂度O(x)；    
**新用户友好**：当用户仅进行少量评分时，即可为其进行较高质量的推荐。

## 参考

[《Slope One Predictors for Online Rating-Based Collaborative Filtering》](https://www.researchgate.net/publication/1960789_Slope_One_Predictors_for_Online_Rating-Based_Collaborative_Filtering)
[Slope One wiki](https://zh.wikipedia.org/wiki/Slope_one)
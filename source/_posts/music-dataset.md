---
title: 音乐数据集汇总
date: 2019-02-13 14:17:57
tags:
- 推荐系统
- 摇滚乐
---

接下来会研究一下音乐推荐系统，需要数据来进行算法及工程代码的演示，遂汇总一下网上开源的音乐数据集。


# Million Song Dataset

说到音乐数据集第一位肯定是MSD，它包含了100万首歌曲的信息，总量有280GB大小。由于数据量的确较大，它使用了h5的文件压缩格式，并提供了一些[code](https://github.com/tbertinmahieux/MSongsDB)用于读这种文件。

<!--more-->

每首歌对应一个文件，字段包括歌曲的方方面面，如 `artist_mbid` ， `artist_name` ， `title` ， `tempo` 等等，所有字段[在这里列出](https://labrosa.ee.columbia.edu/millionsong/pages/example-track-description)。
路径是奇怪的，Q&A中解释说，实在无法把所有文件都放到同一个目录下，目录的组织方式为：
某首歌曲所在位置为它的The Echo Nest track IDs的第三、第四、第五位形成的层级目录，比如 `MillionSong/data/A/D/H/TRADHRX12903CD3866.h5` 。

此外，在MSD的基础上，社区还贡献了不少补充数据集，方便对MSD做各方面的研究。在首页可以很容易找到它们。

-   [The SecondHandSongs Dataset](https://labrosa.ee.columbia.edu/millionsong/secondhand): 一些歌曲被翻唱的信息，以及[Second Hand](https://secondhandsongs.com/)网站对各翻唱的performance值。
-   [The musiXmatch Dataset](https://labrosa.ee.columbia.edu/millionsong/musixmatch): 以bag-of-words的形式提供了MSD中77%数量歌曲的歌词数据。
-   [The Last.fm Dataset](https://labrosa.ee.columbia.edu/millionsong/lastfm): [见下文](#org2ba734e)
-   [The Echo Nest Taste Profile Subset](https://labrosa.ee.columbia.edu/millionsong/tasteprofile): Echo Nest提供了可以与MSD关联的user-song-play count数据集，包含100万user，4800万播放记录。
-   [thisismyjam-to-MSD mapping](https://labrosa.ee.columbia.edu/millionsong/thisismyjam): 音乐社交网站[thisisjam](https://www.thisismyjam.com/)的用户数据以及到MSD的关联。
-   [tagtraum genre annotations](http://www.tagtraum.com/msd_genre_datasets.html): music genre标注。
-   [Top MAGD dataset](http://www.ifs.tuwien.ac.at/mir/msd/): music genre标注。


# Lastfm数据集

[last.fm](https://www.last.fm/)是一家英国的网络电台和音乐社区，其向发开者提供了[丰富的API](https://www.last.fm/api)，于是有很多机构或个人通过调用这些API来生成一些数据集。


## 1K users (user full listening history)

《推荐系统实战》2.1节介绍到了[此数据集](https://www.dtic.upf.edu/~ocelma/MusicRecommendationDataset/lastfm-1K.html)，作为有上下文信息的隐性反馈数据集的代表。
它有两个文件，听歌记录与用户信息。
前者为近1000位听众至2009年5月5日为止的所有音乐播放记录与播放时间，以及音乐的title、artist name、musicbrain id等信息。
后者则记录了所有听众的性别、年龄、国家、注册时间的信息。
其中听歌记录的统计数字如下：

-   Total Lines:           19,150,868
-   Unique Users:                 992
-   Artists with MBID:        107,528
-   Artists without MBDID:     69,420


## 360K users (user top artists)

与1K数据集一起出现的还有360K users数据集。
包含user-artist关系信息以及用户信息。
用户信息与1K相同，不过数据量来到了360K，user-artist关系文件的一行为某user听某乐队的次数。
user-artist文件的统计数据如下：

-   Total Lines:           17,559,530
-   Unique Users:             359,347
-   Artists with MBID:        186,642
-   Artists without MBID:     107,373


## HetRec 2011

这是2011年HetRec会议发布的[从Last.fm获取的数据集](https://grouplens.org/datasets/hetrec-2011/)。
与上两例不同的是它包含有社会好友关系，标签信息。其中文件数目比较多，但各文件列很较少，其中是很明显简单的关联关系，不再赘述。
统计数据如下：

-   1892 users
-   17632 artists
-   12717 好友关系
-   92834 user-listened artist relations
-   11946 tags
-   186479 tag assignments (tas), i.e. tuples [user, tag, artist]


## MSD's Lastfm<a id="org2ba734e"></a>

在MSD的首页可以看到此来自Lastfm的数据集（又一个，真的很容易搞乱。），它作为MSD的补充信息，可与其id直接关联。
数据量较大，是下面的样子：

-   943,347 matched tracks MSD <-> Last.fm
-   505,216 tracks with at least one tag
-   584,897 tracks with at least one similar track
-   522,366 unique tags
-   8,598,630 (track - tag) pairs
-   56,506,688 (track - similar track) pairs

与MSD一样的奇怪的目录结构，每个歌曲对应一个json文件，长这个样子：
![img](http://45.76.195.123/images/2019/06/03/20.jpg)

文件名是 TRAAAAW128F429D538.json 这样的编码可与MSD的某首歌关联起来，图中提供了基本的歌曲、作者信息、标签。
比较独特的是还有Lastfm直接提供的与此歌曲相似的歌曲列表以及相似度值。


# 其他数据集

-   [fma](https://arxiv.org/abs/1612.01840): music audio大型数据集，917 GiB and 343 days of Creative Commons-licensed audio from 106,574 tracks from 16,341 artists and 14,854 albums, arranged in a hierarchical taxonomy of 161 genres。
-   [Pitchfork reviews](https://www.kaggle.com/nolanbconaway/pitchfork-data/home): [Pitchfork](https://pitchfork.com/)是一家在线音乐杂志，有人爬取了自1999年以来的18000份音乐评论文章放到Kaggle上用于分析和学习。 格式为sqlite文件，主要提供信息为文章的id、标题、artist、文章链接、评分、作者、发布时间等。
-   [50 Years of Pop Music Lyrics](https://github.com/walkerkq/musiclyrics): 1964到2015Billboard每年的Year-End Hot100歌曲的歌词。
-   [MetroLyrics](https://www.kaggle.com/gyani95/380000-lyrics-from-metrolyrics/home): 从MetroLyrics爬取的38万首歌词，csv格式，字段有song title，artist，genre，lyric。
-   [kkbox](https://www.kaggle.com/c/kkbox-music-recommendation-challenge): WSDM 2018比赛使用的数据集，[kkbox](https://www.kkbox.com/intl/)作为一家亚洲音乐服务商，提供了很多亚洲歌曲信息，这点是以上其他所不具有的。
-   [Spotify Song Attributes](https://www.kaggle.com/geomack/spotifyclassification/home): 作者调用spotify的api获取了2017首歌的数据并尝试获取训练一个模型来预测自己是否喜欢一首歌。


## API

根据一些官方或民间的API，可以根据自己的需求生成自定义的数据集。

- [last.fm API](https://www.last.fm/api)
- [echonest API](http://developer.echonest.com/)
- [Spotify API](https://developer.spotify.com/documentation/web-api/)
- [The Echo Nest / Spotify APIs work together](http://static.echonest.com/enspex/)
- [music brain API](https://musicbrainz.org/doc/Developer_Resources)
- [云音乐API](https://github.com/yanunon/NeteaseCloudMusic/wiki/网易云音乐API分析)
- [Quora: What is the best, most complete API or database for searching music data?](https://www.quora.com/What-is-the-best-most-complete-API-or-database-for-searching-music-data)
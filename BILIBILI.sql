# 1 视频基本属性
CREATE TABLE Video_basic(
	BVID CHAR(12) PRIMARY KEY, 
    title CHAR(200),
    videos INT, # 分p数
    Tag_partition CHAR(20),
    duration INT
);

# 2 视频热度属性
CREATE TABLE Video_popularity(
	BVID CHAR(12) PRIMARY KEY,
    view BIGINT, #观看数
    barrages BIGINT, # 弹幕数
    reply BIGINT, #评论数
    favorite BIGINT, # 收藏数
    coin BIGINT, # 投币数
    share BIGINT, # 分享数
    likes BIGINT, # 点赞数
    FOREIGN KEY(BVID) REFERENCES Video_basic(BVID)
        ON DELETE CASCADE
);

# 3 弹幕表
CREATE TABLE Barrage(
    BVID CHAR(12),
    Time_in_video DECIMAL(10,2), # 在视频中出现的时间
    Mode INT CHECK(Mode > 0 and Mode < 9), # Mode:1.2.3 滚动弹幕 4.高级弹幕 5.顶端弹幕 6.逆向弹幕 7.精准定位 8.底端弹幕
    Font_size INT, # 字体大小
    Colour CHAR(6),  # 颜色，最后转换成6位的16进制数
    Release_date TIME, # 上传时间
    UP_UID CHAR(20),
    Dtext TEXT, # 弹幕内容
    PRIMARY KEY(UP_UID,BVID,Release_date),
    FOREIGN KEY(BVID) REFERENCES Video_basic(BVID)
        ON DELETE CASCADE,
    FOREIGN KEY(UP_UID) REFERENCES User_basic(UP_UID)
        ON DELETE CASCADE

);

# 4 用户基本属性
CREATE TABLE User_basic(
    UP_UID CHAR(20) PRIMARY KEY,
    nickname CHAR(255), # 昵称
    sex CHAR(1) CHECK(sex in ('F','M','B')), # 女，男，保密
    PersonSign TEXT, # 个性签名
    levels INT, # 等级
    coin FLOAT, # 硬币数
    Vtype INT CHECK(Vtype >= 0 and Vtype <= 2) #(0非会员, 1会员，2年度大会员)
);

# 5 用户热度属性
CREATE TABLE (
    UP_UID CHAR(20) PRIMARY KEY,
    follow BIGINT, # 关注人数
    fan BIGINT, # 粉丝
    likes BIGINT, # 获赞数
    play_amount BIGINT, # 播放量
    reading BIGINT, # 阅读数
    Upload_num BIGINT, # 投稿数
    FOREIGN KEY(UP_UID) REFERENCES User_basic(UP_UID)
        ON DELETE CASCADE
);

# 6 用户投稿表
CREATE TABLE User_Upload(
    UP_UID CHAR(20) PRIMARY KEY,
    video BIGINT, # 视频
    audio BIGINT, # 音频
    article BIGINT, # 专栏
    album BIGINT, # 相簿
    FOREIGN KEY(UP_UID) REFERENCES User_basic(UP_UID)
        ON DELETE CASCADE
);
 
# 7 关系：上传视频
CREATE TABLE Upload_Video(
    UP_UID CHAR(20),
    BVID CHAR(12),
    pubdate TIME, # 上传时间
    ctime TIME, # 审核时间
    PRIMARY KEY(UP_UID,BVID,pubdate),
    FOREIGN KEY(BVID) REFERENCES Video_basic(BVID)
        ON DELETE CASCADE,
    FOREIGN KEY(UP_UID) REFERENCES User_basic(UP_UID)
        ON DELETE CASCADE
);

# 8 番剧数据表
CREATE TABLE Anime_DataItem(
    media_id CHAR(20) PRIMARY KEY, 
    title CHAR(200),    #番剧名称
    Rating DECIMAL(2,1), #评分
    Long_comment INT, #长评数
    Short_comment INT, #短评数
    play BIGINT,      #总播放量
    follow BIGINT,       #追番人数
    barrage BIGINT,      #弹幕数量
    tags SET('原创','漫画改','小说改','游戏改','特摄','布袋戏','热血','穿越','奇幻','战斗','搞笑','日常','科幻','萌系','治愈','校园','少儿','泡面','恋爱','少女','魔法','冒险','历史','架空','机战','神魔','声控','运动','励志','音乐','推理','社团','智斗','催泪','美食','偶像','乙女','职场')   #番剧标签，列表形式
);

# 9 分区表（功能表）
CREATE TABLE Partitions(
    Part_id INT PRIMARY KEY,
    Big_partition CHAR(10), # 大区
    Tag_partition CHAR(15) # 小标签
);

# 10 番剧评论
CREATE TABLE Comment_on_Anime(
    review_id CHAR(20) PRIMARY KEY,
    article_id CHAR(20) DEFAULT NULL,
    media_id CHAR(20), 
    UP_UID CHAR(20),
    Size BOOLEAN, # 0是短评，1是长评==是专栏
    Rating INT CHECK(Rating >= 0 and Rating <= 5), # 评星，0星——5星
    title CHAR(40) DEFAULT NULL, # 长评的标题
    article TEXT NOT NULL, # 文章内容（短评字数限制100，长评字数200~20000)
    ptime TIME, # 发表日期
    FOREIGN KEY(UP_UID) REFERENCES User_basic(UP_UID)
        ON DELETE CASCADE,
    CHECK( (Size = 0 AND LENGTH(article) <= 100) OR (Size = 1 AND LENGTH(article)>= 200 and LENGTH(article) <= 20000) )
);

# 11 视频评论
CREATE TABLE Comment_on_Video(
    Rid CHAR(20),  #评论id
    BVID CHAR(12), #评论的视频
    UP_UID CHAR(20), #评论人
    Ctext TEXT, #评论内容
    ctime TIME, #发送时间
    likes BIGINT, #获赞数
    reply_num BIGINT, #回复数
    Is_reply BOOLEAN, # 是否是回复的评论
    reply_id CHAR(20), #父评论id
    PRIMARY KEY(Rid),
    FOREIGN KEY(BVID) REFERENCES Video_basic(BVID)
        ON DELETE CASCADE,
    FOREIGN KEY(UP_UID) REFERENCES User_basic(UP_UID)
        ON DELETE CASCADE,
    CHECK(Is_reply = 1 OR reply_id != NULL)
);

# 12 专栏数据
CREATE TABLE Article_DataItem(
    CVID CHAR(20) PRIMARY KEY,
    title CHAR(200),    #文章题目
    view BIGINT,    #阅读量
    likes BIGINT,   #喜欢
    reply_num BIGINT,   #回复数
    tags CHAR(10) # 分区（标签）
);

# 13 关系：上传文章
CREATE TABLE Upload_Article(
    CVID CHAR(20) PRIMARY KEY,
    UP_UID CHAR(20),
    pubtime TIME,
    FOREIGN KEY(UP_UID) REFERENCES User_basic(UP_UID)
        ON DELETE CASCADE,
    FOREIGN KEY(CVID) REFERENCES Article_DataItem(CVID)
        ON DELETE CASCADE
);

/*
分区表
(
    生活：
        搞笑
        家居房产
        手工绘画
        日常
    游戏：
        单机游戏
        网络游戏
        手机游戏
        电子竞技
        桌游棋牌
        音游
        GMV
        Mugen
    娱乐：
        综艺
        明星
    知识：
        科学科普
        社科·法律·心理
        人文历史
        财经商业
        校园学习
        职业职场
        设计·创意
        野生技能协会
    影视：
        影视杂谈
        影视剪辑
        短片
        预告·资讯
    音乐：
        原创音乐
        翻唱
        VOCALOID·UTAU
        电音
        演奏
        MV
        音乐现场
        音乐综合
        音频
        说唱
    动画：
        MAD·AMV
        MMD·3D
        短片·手书·配音
        手办·模玩
        特摄
        综合
    时尚：
        美妆护肤
        穿搭
        时尚潮流
    美食：
        美食制作
        美食侦探
        美食测评
        田园美食
        美食记录
    汽车：
        汽车生活
        汽车文化
        汽车极客
        摩托车
        智能出行
        购车攻略
    运动:
        篮球·足球
        健身
        竞技体育
        运动文化
        运动综合
    科技：
        数码
        软件应用
        计算机技术
        工业·工程·机械
        极客DIY
    动物圈：
        喵星人
        汪星人
        大熊猫
        野生动物
        爬宠
        动物综合
    舞蹈：
        宅舞
        街舞
        明星舞蹈
        中国舞
        舞蹈综合
        舞蹈教程
    国创：
        国产动画
        国产原创相关
        布袋戏
        动态漫·广播剧
        资讯
    鬼畜：
        鬼畜调教
        音MAD
        人力VOCALOID
        鬼畜剧场
        教程演示
    纪录片：
        人文·历史
        科学·探索·自然
        军事
        社会·美食·旅行
    番剧：
        资讯
        官方延伸
    电视剧：
        国产剧
        海外剧
    电影：
        国产电影
        欧美电影
        日本电影
        其他国家
)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
*/


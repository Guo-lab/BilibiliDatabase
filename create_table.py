#coding=utf-8

#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

import importlib,sys
importlib.reload(sys)

##################################################
### Python MySQL Has To Execute Single Sentence ##
################################################## 

import pymysql
from pymysql import connect

con = connect(host="127.0.0.1",
              user="root", 
              password="", 
              db="Bilibili", 
              charset='utf8'
              )

cursor = con.cursor()



'''

#sql = """DROP TABLE IF EXISTS Video_basic"""
#cursor.execute(sql)

sql = """
    # 1 视频基本属性
    CREATE TABLE Video_basic(
        BVID CHAR(12) PRIMARY KEY, 
        title CHAR(200),
        videos INT, # 分p数
        Tag_partition CHAR(20),
        duration INT
    );
      """
cursor.execute(sql)

#sql = """DROP TABLE IF EXISTS User_basic"""
#cursor.execute(sql)
sql = """
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
      """
cursor.execute(sql)


#sql = """DROP TABLE IF EXISTS Article_DataItem"""
#cursor.execute(sql)
sql = """
    # 12 专栏数据
    CREATE TABLE Article_DataItem(
        CVID CHAR(20) PRIMARY KEY,
        title CHAR(200),    #文章题目
        view BIGINT,    #阅读量
        likes BIGINT,   #喜欢
        reply_num BIGINT,   #回复数
        tags CHAR(10) # 分区（标签）
    );
      """
cursor.execute(sql)



#sql = """DROP TABLE IF EXISTS Anime_DataItem"""
#cursor.execute(sql)
sql = """
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
      """
cursor.execute(sql)






sql = """DROP TABLE IF EXISTS Video_popularity"""
cursor.execute(sql)
sql = """
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
      """
cursor.execute(sql)



sql = """DROP TABLE IF EXISTS Barrage"""
cursor.execute(sql)
sql = """
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
      """
cursor.execute(sql)








sql = """
    # 5 用户热度属性
    CREATE TABLE Users_popularity (
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
      """
cursor.execute(sql)



sql = """
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
      """
cursor.execute(sql)



sql = """
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
      """
cursor.execute(sql)





sql = """
    # 9 分区表（功能表）
    CREATE TABLE Partitions(
        Part_id INT PRIMARY KEY,
        Big_partition CHAR(10), # 大区
        Tag_partition CHAR(15) # 小标签
    );
      """
cursor.execute(sql)





sql = """
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
      """
cursor.execute(sql)





sql = """
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
      """
cursor.execute(sql)




sql = """
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
      """
cursor.execute(sql)




#cursor.execute("INSERT INTO STU (`FIRST_NAME`, `AGE`, `ID`) VALUES('GUO', 18, 1)" )
#con.commit()


#cursor.execute("SELECT * FROM STU")
#results = cursor.fetchall()
#for row in results:
#    fname = row[0]
#    age = row[1]
#    id = row[2]



print("MySQL CREATED TABLE SUCCESSFULLY!")



sql = """
        INSERT INTO `Bilibili`.`Video_basic` (`BVID`, `title`, `videos`, `Tag_partition`, `duration`) VALUES ('BVID30193', 'LOL', 1, 'game', 141);
      """
cursor.execute("INSERT INTO Video_basic (`BVID`,`title`,`videos`,`Tag_partition`, `duration`) VALUES ('BV1i34112729', 'ab', 1, 'c' ,141);")
con.commit()

sql = "INSERT INTO `Bilibili`.`Video_basic` (`BVID`, `title`, `videos`, `Tag_partition`, `duration`) VALUES ('BVID3001', 'gg', 2, 'B', 40);"
cursor.execute(sql)
con.commit()



sql = "INSERT INTO `Bilibili`.`Article_DataItem` (`CVID`, `title`, `view`, `likes`, `reply_num`, `tags`) VALUES ('CVID00001', 'gg', 500, 30, 20, 'gg');"
cursor.execute(sql)
con.commit()



sql = "INSERT INTO `Bilibili`.`User_basic` (`UP_UID`, `nickname`, `sex`, `PersonSign`, `levels`, `coin`, `Vtype`) VALUES ('UP_UID5066', 'gsq', 'M', 'HELLO', 100, 10000, 1);"
cursor.execute(sql)
con.commit()


sql = "INSERT INTO `Bilibili`.`Anime_DataItem` (`media_id`, `title`, `Rating`, `Long_comment`, `Short_comment`, `play`, `follow`, `barrage`, `tags`) VALUES ('00000000', '鬼灭之刃', 9.7, 664, 7343434, 7200000, 343949, 555, '');"
cursor.execute(sql)
con.commit()



sql = "INSERT INTO `Bilibili`.`Partitions` (`Part_id`, `Big_partition`, `Tag_partition`) VALUES (0, '生活', '搞笑');"
cursor.execute(sql)
con.commit()

sql = "INSERT INTO `Bilibili`.`Upload_Article` (`CVID`, `UP_UID`, `pubtime`) VALUES ('CVID00001', 'UP_UID5066', '00:00:00');"
cursor.execute(sql)
con.commit()

sql = "INSERT INTO `Bilibili`.`User_Upload` (`UP_UID`, `video`, `audio`, `article`, `album`) VALUES ('UP_UID5066', NULL, NULL, NULL, NULL);"
cursor.execute(sql)
con.commit()




sql = """
# 1 计算该用户的投稿数
        CREATE DEFINER=`root`@`localhost` PROCEDURE `sum_of_upload`(
            IN UP_UID CHAR(20),
            OUT upload_num BIGINT
        )
        BEGIN 
            declare video_num bigint;
            declare audio_num bigint;
            declare article_num bigint;
            declare album_num bigint;

            set video_num = (select video from user_upload where UP_UID = new.UP_UID);
            set audio_num = (select audio from user_upload where UP_UID = new.UP_UID);
            set article_num = (select article from user_upload where UP_UID = new.UP_UID);
            set album_num = (select album from user_upload where UP_UID = new.UP_UID);
            
            set Upload_num = video_num + audio_num + article_num + album_num;
        END;
      """
cursor.execute(sql)
con.commit()




sql = """
        # 2 用户注册，创建初始表
        CREATE DEFINER=`root`@`localhost` PROCEDURE `new_user`(
            IN UP_UID CHAR(20),
            IN nickname CHAR(255),
            IN sex CHAR(1),
            IN PersonSign TEXT
        )
        BEGIN
            INSERT INTO User_basic VALUES(UP_UID,nickname,sex,PersonSign,0,0,0);
        END
      """
cursor.execute(sql)
con.commit()


sql = """
        # 3 用户答题及格，成为会员，创建热度表
        CREATE DEFINER=`root`@`localhost` PROCEDURE `new_vipUser`(
            IN UP_UID CHAR(20)
        )
        BEGIN
            INSERT INTO User_popularity VALUES(UP_UID,0,0,0,0,0,0);
        END
      """
cursor.execute(sql)
con.commit()  



sql = """
        # 4 用户上传视频(过审、发布)
        CREATE DEFINER=`root`@`localhost` PROCEDURE `user_upload_viedo`(
            IN UP_UID CHAR(20),
            IN pubdate DATE,
            IN title CHAR(200),
            IN videos INT,
            IN Tag_partition CHAR(20),
            IN duration INT
        )
        BEGIN
            DECLARE ctime DATE;
            DECLARE BVID CHAR(12);

            set BVID = get_BVID();
            set ctime = current_data();

            INSERT INTO upload_video VALUES(UP_UID,BVID,pubdate,ctime);
            INSERT INTO Video_basic VALUES(BVID,title,videos,Tag_partition,duration);
            INSERT INTO Video_popularity VALUES(BVID,0,0,0,0,0,0,0,0);
        END
      """
cursor.execute(sql)
con.commit()     



sql = """
        # 5 用户上传文章(过审、发布)
        CREATE DEFINER=`root`@`localhost` PROCEDURE `user_upload_article`(
            IN UP_UID CHAR(20),
            IN title CHAR(200),
            IN tags CHAR(10)
        )
        BEGIN
            DECLARE CVID CHAR(20);
            DECLARE ptime DATE;

            set CVID = get_CVID();
            set ptime = current_data();

            INSERT INTO Article_DataItem VALUES(CVID,title,0,0,0,tags);
            INSERT INTO Upload_Article values(CVID,UP_UID,ptime);
        END
      """
cursor.execute(sql)
con.commit()  


sql = """
        # 6 获得可用的BV号
        CREATE DEFINER=`root`@`localhost` FUNCTION `get_BVID`() 
        RETURNS char(1) CHARSET utf8mb4
            DETERMINISTIC
        BEGIN
            DECLARE id bigint;
            DECLARE success BOOLEAN;
            declare idc char(12);
            
            set success = 0;
            set id = 0;
            
            while success != 1 
            do
                set idc = cast(a as char(12));
                if idc in (select BVID from Video_basic) 
                then
                    set id = id + 1;
                else
                    set success = 1;
                end if;
            end while;
            RETURN idc;
        END
      """
cursor.execute(sql)
con.commit() 


sql = """
        # 7 番剧上架，创建对应数据表
        CREATE DEFINER=`root`@`localhost` PROCEDURE `new_anime`(
            IN title CHAR(200),
            IN tags SET('原创','漫画改','小说改','游戏改','特摄','布袋戏','热血','穿越','奇幻','战斗','搞笑','日常','科幻','萌系','治愈','校园','少儿','泡面','恋爱','少女','魔法','冒险','历史','架空','机战','神魔','声控','运动','励志','音乐','推理','社团','智斗','催泪','美食','偶像','乙女','职场')
        )
        BEGIN
            DECLARE MID CHAR(20);
            set MID = get_MID();

            INSERT INTO Anime_DataItem values(MID,title,0,0,0,0,0,0,tags);
        END
      """
cursor.execute(sql)
con.commit()   


sql = """ show table status;
      """
display = cursor.execute(sql)
#con.commit()          
print(display)



sql = """ DELETE FROM Video_basic WHERE BVID ='BV0000000006'; """
cursor.execute(sql)
con.commit()



sql = """
UPDATE Video_basic SET title='KK', videos=2, Tag_partition='richang', duration=141 WHERE BVID='BV0000000001';
      """
cursor.execute(sql)
con.commit()


sql = """
    LOAD DATA INFILE '/Users/gsq/Desktop/DatabasePractice/Final/csv/user_info.csv' INTO TABLE User_basic 
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' 
    LINES TERMINATED BY '\r\n\';
      """
cursor.execute(sql)
con.commit()


'''






'''
# .src 中有 pymysql.err.IntegrityError: (1062, "Duplicate entry '1023724342' for key 'user_link.PRIMARY'")
sql = """
    CREATE TABLE media_link(
        media_id CHAR(100) PRIMARY KEY,
        name CHAR(100),
        link TEXT
    );
      """
cursor.execute(sql)
con.commit()

sql = """
    LOAD DATA INFILE '/Users/gsq/Desktop/DatabasePractice/Final/csv_link/media_link_src.csv' INTO TABLE media_link 
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' 
    LINES TERMINATED BY '\r\n\';
      """
cursor.execute(sql)
con.commit()

'''

'''
sql = """    
    CREATE TABLE user_link(
        id integer(255) auto_increment primary key,
        uid CHAR(100),
        name CHAR(100),
        link TEXT 
    );
      """
cursor.execute(sql)
con.commit()
'''


sql = """
    CREATE TABLE video_link(
        id integer(255) auto_increment primary key,
        bvid CHAR(100),
        name CHAR(100),
        link TEXT 
    );
      """
cursor.execute(sql)
con.commit()


'''
sql = """
    LOAD DATA INFILE '/Users/gsq/Desktop/DatabasePractice/Final/csv_link/user_link_src.csv' INTO TABLE user_link
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' 
    LINES TERMINATED BY '\r\n\';
      """
cursor.execute(sql)
con.commit()
'''

sql = """
    LOAD DATA INFILE '/Users/gsq/Desktop/DatabasePractice/Final/csv_link/video_link_src.csv' INTO TABLE video_link 
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' 
    LINES TERMINATED BY '\r\n\';
      """
cursor.execute(sql)
con.commit()




print("INSERT DONE!")


con.close()



'''
import flasks
sys.path.append (r"/Users/gsq/Desktop/DatabasePractice/Final/")
flasks.app.run()
'''
import requests
import json
import csv
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
def get_many_uid(uid_list):
    url="https://api.bilibili.com/x/v2/reply?type=1&oid="
    av='715024588'
    html=url+av+'&pn='
    count=1
    midlist = []
    while(True):
        if count==5:                            #爬取5页评论
            break
        url=html+str(count)
        url=requests.get(url)
        if url.status_code==200:
            cont=json.loads(url.text)
        else:
            break
        lengthRpy = len(cont['data']['replies'])
        if lengthRpy!=0:
            for i in range(lengthRpy):
                uid_num=cont['data']['replies'][i]['member']['mid']
                uid_list.append([uid_num])
                leng=len(cont['data']['replies'][i]['replies'])
                for j in range(leng):
                    uid_num=cont['data']['replies'][i]['replies'][j]['member']['mid']
                    uid_list.append(uid_num)
        else :
            break
        print("第%d页uid写入成功！"%count)
        count += 1
    print(count-1,'页uid写入成功!   共',len(uid_list),"个uid")
def get_many_media_id(media_list) :
    url = 'https://api.bilibili.com/pgc/season/index/result?season_version=-1&spoken_language_type=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page='
    mid = '&season_type=1&pagesize=20&type=1'
    for i in range(1,4) :    #可调爬取页数
        html = url + str(i) + mid
        html = requests.get(html)
        cont=json.loads(html.text)
        #print(cont)
        #print("len: "+len(cont['data']['list']))
        for j in range(len(cont['data']['list'])) :
            media_id = cont['data']['list'][j]['media_id']
            media_list.append(media_id)

def get_info_user(uid_list):
    headers = {
          'User-Agent':'Mozilla/5.0',
    }
    html="https://api.bilibili.com/x/space/acc/info?mid="
    midlist = []
    for i in uid_list :
        url = html + str(i)
        url=requests.get(url,  headers=headers)
        if url.status_code==200:
            cont=json.loads(url.text)
        else:
            break
        up_uid = str(i)
        nickname = cont['data']['name']
        if cont['data']['sex'] == '保密' :
            sex = 'B'
        elif cont['data']['sex'] == '女' :
            sex = 'F'
        else :
            sex = 'M'
        person_sign = cont['data']['sign']
        level = cont['data']['level']
        coin = cont['data']['coins']
        vtype = cont['data']['vip']['type']
        #print(nickname)
        midlist.append([up_uid, nickname, sex, person_sign, level, coin, vtype])
    with open('user_info.csv','w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["UID", "昵称", "性别", "标语", "等级", "投币", "会员等级"])
        for info in midlist:
            writer.writerow(info)
    print("写入成功!    一共",len(midlist),"个up主信息")
def get_user_popularity(uid_list):
    headers = {
          'User-Agent':'Mozilla/5.0',
    }
    html_1 = "https://api.bilibili.com/x/relation/stat?vmid="    #粉丝，关注
    html_2 = "https://api.bilibili.com/x/space/upstat?mid="      #播放，阅读，点赞
    html_3 = "https://api.bilibili.com/x/space/arc/search?mid="  #投稿
    midlist = []
    for i in uid_list :
        url_1 = html_1 + str(i)
        url_1 = requests.get(url_1,  headers=headers)
        cont_1 = json.loads(url_1.text)
        follow = cont_1['data']['following']
        fan = cont_1['data']['follower']

        url_2 = html_2 + str(i)
        url_2 = requests.get(url_2,  headers=headers)
        cont_2 = json.loads(url_2.text)
        likes = cont_2['data']['likes']
        play_account = cont_2['data']['archive']['view']
        reading = cont_2['data']['article']['view']

        url_3 = html_3 + str(i)
        url_3 = requests.get(url_3,  headers=headers)
        cont_3 = json.loads(url_3.text)
        load_num = cont_3['data']['page']['count']
        
        uid = str(i)
        midlist.append([uid, follow, fan, likes, play_account, reading, load_num])
    with open('user_popularity.csv','w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["uid", "follow", "fan", "likes", "play_account", "reading", "load_num"])
        for info in midlist:
            writer.writerow(info)  
    print("用户popularity信息写入完成！ 共",len(midlist),"个用户信息") 
def get_user_load(uid_list) :
    url = "https://api.bilibili.com/x/space/navnum?mid=6075139"

def get_video_basic(bv_list):
    headers = {
          'User-Agent':'Mozilla/5.0',
    }
    html="https://api.bilibili.com/x/web-interface/view?cid=141553944&bvid="
    midlist = []
    for i in bv_list :
        url = html + str(i)
        url=requests.get(url,  headers=headers)
        if url.status_code==200:
            cont=json.loads(url.text)
        else:
            break
        bvid = str(i)
        vedios = cont['data']['videos']
        duration = cont['data']['duration']
        title = cont['data']['title']
        tag = cont['data']['tname']
        midlist.append([bvid, title, vedios, tag, duration])
    with open('video_basic.csv','w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["bvid", "title", "vedios", "tag", "duration"])
        for info in midlist:
            writer.writerow(info)
    print("视频基本信息写入完成！ 共",len(midlist),"个视频")
def get_vedio_popularity(bv_list):
    headers = {
          'User-Agent':'Mozilla/5.0',
    }
    html="https://api.bilibili.com/x/web-interface/archive/stat?bvid="
    midlist = []
    for i in bv_list :
        url = html + str(i)
        url=requests.get(url,  headers=headers)
        if url.status_code==200:
            cont=json.loads(url.text)
        else:
            break
        bvid = str(i)
        view = cont['data']['view']
        danmaku = cont['data']['danmaku']
        reply = cont['data']['reply']
        favorite = cont['data']['favorite']
        coin = cont['data']['coin']
        share = cont['data']['share']
        likes = cont['data']['like']
        midlist.append([bvid, view, danmaku, reply, favorite, coin, share, likes])
    with open('vedio_popularity.csv','w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["bvid", "view", "danmaku", "reply", "favorite", "coin", "share", "likes"])
        for info in midlist:
            writer.writerow(info)
    print("视频popularity写入完成！ 共",len(midlist),"个视频")
def get_danmu(bv_list):
    headers = {
          'User-Agent':'Mozilla/5.0',
        }
    for i in bv_list :
        BVName = str(i)
        url = 'https://www.bilibili.com/video/' + BVName
        resp = requests.get(url, headers=headers)
        match_rule = r'cid=(.*?)&aid'
        oid = re.search(match_rule ,resp.text).group().replace('cid=','').replace('&aid','')
        xml_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid='+oid
        resp = requests.get(xml_url, headers=headers)
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, 'html.parser')
        danmu_list = soup.findAll('d')
        all_danmu = []
        for item in danmu_list:
            item_list = item.attrs['p'].split(',')
            item_list[3] = '0x{:06X}'.format(int(item_list[3]))

            time_l = time.localtime(int(item_list[4]))
            year = time_l.tm_year
            month = time_l.tm_mon
            day = time_l.tm_mday
            c_time = str(year)+"-"+str(month)+"-"+str(day)

            mid_list = [BVName, item_list[0], item_list[1], item_list[2],
                        item_list[3], c_time, item_list[6], item.text]
            all_danmu.append(mid_list)
            columns = ['BV号', '出现时间', '弹幕类型', '字的大小', '颜色', '上传时间', 'uid', '弹幕内容']
            danmu_df = pd.DataFrame(all_danmu, columns=columns)
            save_path = 'danmu.csv'
            danmu_df.to_csv(save_path, index=False)
        print(BVName + ' done!  共',len(danmu_list),"个弹幕")
    print("弹幕爬取完成")
def get_comment(bv_list):
    headers = {
          'User-Agent':'Mozilla/5.0',
        }
    midlist = []
    for k in bv_list :
        BVName = str(k)
        url = "https://api.bilibili.com/x/web-interface/view?cid=141553944&bvid=" + BVName
        url = requests.get(url, headers=headers)
        resp = json.loads(url.text)
        aid = str(resp['data']['aid'])
        url = 'https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=' + aid
        url=requests.get(url)
        if url.status_code==200:
            cont=json.loads(url.text)
        else:
            break
        lengthRpy = len(cont['data']['replies'])
        for i in range(lengthRpy):
            bv_id = BVName
            r_id = str(cont['data']['replies'][i]['rpid'])
            commentator = str(cont['data']['replies'][i]['member']['mid'])
            ctext = cont['data']['replies'][i]['content']['message']

            time_l = time.localtime(cont['data']['replies'][i]['ctime'])
            year = time_l.tm_year
            month = time_l.tm_mon
            day = time_l.tm_mday
            c_time = str(year)+"-"+str(month)+"-"+str(day)

            likes = cont['data']['replies'][i]['like']
            reply_num = len(cont['data']['replies'][i]['replies'])
            if reply_num == 0 :
                is_reply = 0
            else :
                is_reply = 1
            reply_id = 0
            midlist.append([r_id, bv_id, commentator, ctext, c_time, likes, reply_num, is_reply, reply_id])
            leng=len(cont['data']['replies'][i]['replies'])
            for j in range(leng):
                s_bv_id = BVName
                s_r_id = str(cont['data']['replies'][i]['replies'][j]['rpid'])
                s_commentator = str(cont['data']['replies'][i]['replies'][j]['member']['mid'])
                s_ctext = cont['data']['replies'][i]['replies'][j]['content']['message']

                time_l = time.localtime(cont['data']['replies'][i]['replies'][j]['ctime'])
                year = time_l.tm_year
                month = time_l.tm_mon
                day = time_l.tm_mday
                s_c_time = str(year)+"-"+str(month)+"-"+str(day)

                s_likes = cont['data']['replies'][i]['replies'][j]['like']
                s_reply_num = 0
                s_is_reply = 0
                s_reply_id = str(cont['data']['replies'][i]['replies'][j]['parent_str'])
                midlist.append([s_r_id, s_bv_id, s_commentator, s_ctext, s_c_time, s_likes, s_reply_num, s_is_reply, s_reply_id])
        with open('comments.csv','w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["r_id", "bvid", "commentator", "ctext", "c_time", "likes", "reply_num", "is_reply", "reply_id"])
            for info in midlist:
                writer.writerow(info)
        print(BVName + ' done!  共',len(midlist),"个评论")
    print("评论爬取完成")
def get_upload_vedio(bv_list):
    headers = {
          'User-Agent':'Mozilla/5.0',
    }
    html="https://api.bilibili.com/x/web-interface/view?cid=141553944&bvid="
    midlist = []
    for i in bv_list :
        url = html + str(i)
        url=requests.get(url,  headers=headers)
        if url.status_code==200:
            cont=json.loads(url.text)
        else:
            break
        bvid = str(i)
        up_uid = str(cont['data']['owner']['mid'])

        time_l = time.localtime(cont['data']['pubdate'])
        year = time_l.tm_year
        month = time_l.tm_mon
        day = time_l.tm_mday
        pubdate = str(year)+"-"+str(month)+"-"+str(day)

        time_l = time.localtime(cont['data']['ctime'])
        year = time_l.tm_year
        month = time_l.tm_mon
        day = time_l.tm_mday
        ctime = str(year)+"-"+str(month)+"-"+str(day)
        midlist.append([up_uid, bvid, pubdate, ctime])
    with open('upload_vedio.csv','w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["up_uid", "bvid", "pubdate", "ctime"])
        for info in midlist:
            writer.writerow(info)
    print("视频上载信息写入完成！ 共",len(midlist),"个视频")
def get_anime_data(media_list) :
    mid = 'https://www.bilibili.com/bangumi/media/md'
    midlist = []
    for i in media_list :
        media_id = i
        url = mid + str(media_id)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")
        item =soup.find_all('div',class_="media-detail-wrp")[0]
        item = str(item)

        name=re.findall(r'<span class="media-info-title-t">(.*?)</span>',item)[0]
        score=re.findall(r'<div class="media-info-score-content">(.*?)</div>',item)[0]
        longc=re.findall(r'长评 \( (\d+) \)',item)[0]
        shortc=re.findall(r'短评 \( (\d+) \)',item)[0]
        play=re.findall(r'<em>(.*?)</em>',item)[0]
        follow=re.findall(r'<em>(.*?)</em>',item)[1]
        danmu=re.findall(r'<em>(.*?)</em>',item)[2]
        tag=re.findall(r'<span class="media-tag">(.*?)</span>',item)
        midlist.append([media_id, name, score, longc, shortc, play, follow, danmu, tag])
    with open('anime_data.csv','w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["media_id", "name", "score", "longc", "shortc", "play", "follow", "danmu", "tag"])
        for info in midlist:
            writer.writerow(info)  
    print("番剧信息写入完成！ 共",len(midlist),"个番剧信息") 
def get_anime_comment(media_list) :
    mid_1 = 'https://api.bilibili.com/pgc/review/long/list?media_id='   #长评API
    mid_2 = 'https://api.bilibili.com/pgc/review/short/list?media_id='  #短评API
    midlist = []
    for i in media_list :
        media_id = str(i)
        url_1 = mid_1 + str(i)
        url_2 = mid_2 + str(i)
        html_1 = requests.get(url_1)
        html_2 = requests.get(url_2)
        cont_1 = json.loads(html_1.text)
        cont_2 = json.loads(html_2.text)

        #获取长评信息
        for j in range(len(cont_1['data']['list'])) :
            uid = str(cont_1['data']['list'][j]['author']['mid'])
            article_id = cont_1['data']['list'][j]['article_id']
            review_id = str(cont_1['data']['list'][j]['review_id'])
            size = 1
            rating = cont_1['data']['list'][j]['score']/2
            title = cont_1['data']['list'][j]['title']
            article = cont_1['data']['list'][j]['content']

            time_l = time.localtime(cont_1['data']['list'][j]['ctime'])
            year = time_l.tm_year
            month = time_l.tm_mon
            day = time_l.tm_mday
            ptime = str(year)+"-"+str(month)+"-"+str(day)

            midlist.append([review_id, article_id, media_id, uid, size, rating, title, article, ptime])

        #获取短评信息
        for j in range(len(cont_1['data']['list'])) :
            uid = str(cont_2['data']['list'][j]['author']['mid'])
            article_id = 0
            review_id = str(cont_1['data']['list'][j]['review_id'])
            size = 0
            rating = cont_2['data']['list'][j]['score']/2
            title = ""
            article = cont_2['data']['list'][j]['content']

            time_l = time.localtime(cont_2['data']['list'][j]['ctime'])
            year = time_l.tm_year
            month = time_l.tm_mon
            day = time_l.tm_mday
            ptime = str(year)+"-"+str(month)+"-"+str(day)

            midlist.append([review_id, article_id, media_id, uid, size, rating, title, article, ptime])
    with open('anime_comment.csv','w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["review_id", "article_id", "media_id", "uid", "size", "ratings", "title", "article", "ptime"])
        for info in midlist:
            writer.writerow(info)  
    print("番剧评论信息写入完成！ 共",len(media_list),"个番剧信息") 

def get_article_data(cv_list, c_mid, cv_time) :
    html = 'https://api.bilibili.com/x/article/recommends?cid=0&pn=1&ps=20&jsonp=jsonp&aids=&sort=0'
    midlist = []
    for i in range(0,3) :         #设置爬取次数
        url = requests.get(html)
        if url.status_code==200:
            cont=json.loads(url.text)
        else:
            break
        length = len(cont['data'])
        for j in range(length) :
            cvid = str(cont['data'][j]['id'])
            if cvid in cv_list:
                continue
            cv_list.append(cvid)
            uid = cont['data'][j]['author']['mid']
            c_mid.append(uid)
            publish_time = cont['data'][j]['publish_time']
            cv_time.append(publish_time)

            title = cont['data'][j]['title']
            view = cont['data'][j]['stats']['view']
            likes = cont['data'][j]['stats']['like']
            reply = cont['data'][j]['stats']['reply']
            tag = cont['data'][j]['category']['name']
            midlist.append([cvid, title, view, likes, reply, tag])
    with open('article_data.csv','w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["cvid", "title", "view", "likes", "reply", "tag"])
        for info in midlist:
            writer.writerow(info)
    print("文章信息写入完成！ 共",len(midlist),"个文章")
def get_upload_aricle(cv_list, c_mid, cv_time) :
    url = "https://www.bilibili.com/read/cv"
    midlist = []
    for i in range(len(cv_list)) :
        cvid = cv_list[i]
        uid = c_mid[i]
        time_l = time.localtime(cv_time[i])
        year = time_l.tm_year
        month = time_l.tm_mon
        day = time_l.tm_mday
        p_time = str(year)+"-"+str(month)+"-"+str(day)
        midlist.append([cvid, uid, p_time])
    with open('upload_aricle.csv','w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["cvid", "uid", "p_time"])
        for info in midlist:
            writer.writerow(info)  
    print("文章上载信息写入完成！ 共",len(midlist),"个文章信息") 

def creat_tag(b_tag,s_tag) :
    midlist = []
    for i in range(len(b_tag)):
        for j in range(len(s_tag[i])):
            tid = i*100+j
            big = b_tag[i]
            small = s_tag[i][j]
            midlist.append([tid,big,small])
    with open('tag.csv','w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["tid", "big_tag", "small_tag"])
        for info in midlist:
            writer.writerow(info)
    print("分区信息写入完成")

def get_user_link() :
    url="https://api.bilibili.com/x/v2/reply?type=1&oid="
    av='715024588'
    html=url+av+'&pn='
    count=1
    link_mid = 'https://space.bilibili.com/'
    midlist = []
    while(True):
        if count==10:                          
            break
        url=html+str(count)
        url=requests.get(url)
        if url.status_code==200:
            cont=json.loads(url.text)
        else:
            break
        lengthRpy = len(cont['data']['replies'])
        if lengthRpy!=0:
            for i in range(lengthRpy):
                uid_num=cont['data']['replies'][i]['member']['mid']
                name = cont['data']['replies'][i]['member']['uname']
                link = link_mid + str(uid_num)
                midlist.append([uid_num,name,link])
                leng=len(cont['data']['replies'][i]['replies'])
                for j in range(leng):
                    uid_num=cont['data']['replies'][i]['replies'][j]['member']['mid']
                    name = cont['data']['replies'][i]['replies'][j]['member']['uname']
                    link = link_mid + str(uid_num)
                    midlist.append([uid_num,name,link])
        else :
            break
        count += 1
    with open('user_link.csv','w', encoding='utf-8') as f:
        writer = csv.writer(f)
        #writer.writerow(["uid", "name", "link"])
        for info in midlist:
            writer.writerow(info)  
    print("用户链接信息写入完成！ 共",len(midlist),"个用户信息") 
def get_media_link():
    html = 'https://api.bilibili.com/pgc/season/index/result?season_version=-1&spoken_language_type=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page='
    mid = '&season_type=1&pagesize=20&type=1'
    midlist = []
    link_mid = 'https://www.bilibili.com/bangumi/media/md'
    for i in range(1,10):
        url = html + str(i) + mid
        url = requests.get(url)
        cont=json.loads(url.text)
        for i in range(len(cont['data']['list'])) :
            name = cont['data']['list'][i]['title']
            media_id = cont['data']['list'][i]['media_id']
            link = link_mid + str(media_id)
            midlist.append([media_id,name,link])
    with open('media_link.csv','w', encoding='utf-8') as f:
        writer = csv.writer(f)
        #writer.writerow(["media_id", "name", "link"])
        for info in midlist:
            writer.writerow(info)  
    print("番剧链接信息写入完成！ 共",len(midlist),"个番剧信息") 
def get_video_link() :
    html = 'https://api.bilibili.com/x/web-interface/web/channel/category/channel_arc/list?id=0&offset='
    midlist = []
    for k in range(0,5):
        url=requests.get(html+str(k*6))
        cont=json.loads(url.text)
        classes = cont['data']['archive_channels']
        link_mid = 'https://www.bilibili.com/video/'
        for i in range(len(classes)):
            m_classes = cont['data']['archive_channels'][i]['archives']
            for j in range(len(m_classes)) :
                name = cont['data']['archive_channels'][i]['archives'][j]['name']
                bvid = cont['data']['archive_channels'][i]['archives'][j]['bvid']
                link = link_mid + str(bvid)
                midlist.append([bvid,name,link])
    with open('video_link.csv','w', encoding='utf-8') as f:
        writer = csv.writer(f)
        #writer.writerow(["bvid", "name", "link"])
        for info in midlist:
            writer.writerow(info)  
    print("视频链接信息写入完成！ 共",len(midlist),"个视频信息") 

if __name__ == '__main__':
    uid_list = ['434794434']
    bv_list = ['BV1i34112729']
    media_list = ['22718131']
    cv_list = []
    c_mid = []
    cv_time = []
    b_tag = ["生活","游戏","娱乐","影视","音乐","动画","时尚","美食","汽车","运动","科技","动物圈","舞蹈","国创","鬼畜","纪录片","番剧","电视剧","电影"]
    s_tag = [["搞笑","家居房产","手工绘画","日常","知识"],
            ["单机游戏","网络游戏","手机游戏","电子竞技","桌游棋牌","音游","GMV","Mugen"],
            ["综艺","明星"],
            ["科学科普","社科·法律·心理","人文历史","财经商业","校园学习","职业职场","设计·创意","野生技能协会"],
            ["影视杂谈","影视剪辑","短片","预告·资讯"],
            ["原创音乐","翻唱","VOCALOID·UTAU","电音","演奏","MV","音乐现场","音乐综合","音频","说唱"],
            ["MAD·AMV","MMD·3D","短片·手书·配音","手办·模玩","特摄","综合"],
            ["美妆护肤","穿搭","时尚潮流"],
            ["美食制作","美食侦探","美食测评","田园美食","美食记录"],
            ["汽车生活","汽车文化","汽车极客","摩托车","智能出行","购车攻略"],
            ["篮球·足球","健身","竞技体育","运动文化","运动综合"],
            ["数码","软件应用","计算机技术","工业·工程·机械","极客DIY"],
            ["喵星人","汪星人","大熊猫","野生动物","爬宠""动物综合"],
            ["宅舞","街舞","明星舞蹈","中国舞","舞蹈综合","舞蹈教程"],
            ["国产动画","国产原创相关","布袋戏","动态漫·广播剧","资讯"],
            ["鬼畜调教","音MAD","人力VOCALOID","鬼畜剧场","教程演示"],
            ["人文·历史","科学·探索·自然","军事","社会·美食·旅行"],
            ["资讯","官方延伸"],
            ["国产剧","海外剧"],
            ["国产电影","欧美电影","日本电影","其他国家"]]

    # get_many_uid(uid_list)
    # print(uid_list)
    # get_many_media_id(media_list)
    # print(media_list)

    # #爬取用户基本信息
    # get_info_user(uid_list)
    # #爬取用户popularity信息
    # # get_user_popularity(uid_list)
    # #爬取用户上载信息
    # # get_user_load(uid_list)

    # #爬取视频基本信息
    # get_video_basic(bv_list)
    # #爬取视频popularity
    # get_vedio_popularity(bv_list)
    # #爬取弹幕信息
    # get_danmu(bv_list)
    # #爬取评论
    # get_comment(bv_list)
    # #爬取视频上载信息
    # get_upload_vedio(bv_list)

    # #爬取番剧基本信息
    # get_anime_data(media_list)
    # #爬取番剧评论信息
    # get_anime_comment(media_list)

    # #get_article_data要先于get_upload_article执行
    # #爬取文章信息
    # get_article_data(cv_list, c_mid, cv_time)
    # #获取文章上载信息
    # get_upload_aricle(cv_list, c_mid, cv_time)

    # creat_tag(b_tag,s_tag)

    #爬取用户--姓名--链接信息
    get_user_link()
    #爬取番剧--姓名--链接信息
    get_media_link()
    #爬取视频--名称--链接信息
    get_video_link()
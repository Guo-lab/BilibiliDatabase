#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask, render_template, request, jsonify, redirect, url_for

# To Paginate
from flask_sqlalchemy import SQLAlchemy
#from flask_paginate import Pagination, get_page_parameter

# For Rendering
from flask_bootstrap import Bootstrap

#%pip install --upgrade flask_nav
from flask_nav import Nav
from flask_nav.elements import *
from flask_nav.elements import Navbar, View, Subgroup, Separator, Text, Link
#from flask.ext.navigation import Navigation


# Database pymysql
from database_class import Database


# Unicode Url_for
import urllib
#from urllib import parse
#from urlparse import urlparse
#from string import maketrans










#############################################################
####################### Navigator ###########################
nav = Nav()

@nav.navigation()
def top_nav():
    return Navbar(
                u'数据库小假期实践',
                View('Home', 'root'),
                View('Users Register', 'users'),
                Subgroup(
                    'Tables',
                    View('Video_basic', 'Video_basic'),
                    View('User_basic', 'User_basic'),
                    View('Article_DataItem', 'Article_DataItem'),
                    View('Anime_DataItem', 'Anime_DataItem'),
                    View('Partitions', 'Partitions'),
                    Separator(),
                    View('User_Upload', 'User_Upload'),
                    View('Upload_Article', 'Upload_Article'),
                    View('Upload_Video', 'Upload_Video'),
                    Separator(),
                    View('Barrage', 'Barrage'),
                    View('Comment_on_Anime', 'Comment_on_Anime'),
                    View('Comment_on_Video', 'Comment_on_Video'),
                    View('Video_popularity', 'Video_popularity'),
                    Separator(),
                    Text('Other Tables'),
                    View('...', 'whatsup'),
                ),
                Subgroup(
                    'Links Table',
                    View('media_link', 'media_link'),
                    View('user_link', 'user_link'),
                    View('video_link', 'video_link'),
                ),
                Subgroup(
                    'Tech Support',
                    Link('TechSupport_src', 'http://techsupport.invalid/widgits_inc'),
                    Link('flask-nav', 'https://www.cnblogs.com/wongbingming/p/6813221.html'),
                    Link('Runoob', 'https://www.runoob.com/bootstrap/bootstrap-typography.html'),
                    Link('Style-css', 'https://www.bootstrapcdn.com/bootswatch/')
                ),
                View('About', 'about')
        )




# registers the "top" menubar
nav.register_element('top', top_nav) 

                        

app = Flask(__name__)
Bootstrap(app)


nav.init_app(app)









##############################################################
######################### SQLAlchemy #########################
##############################################################
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/Bilibili'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

'''
def create():
    db.create_all()
    lis = []
    for i in range(10):
        admin = User(username='admin_%s' % i, email='admin_%s@example.com' % i )
        db.session.add(admin)
        db.session.commit()
'''













##############################################################
######################### Flask ##############################
################## . #########################################
@app.route("/")
def root():
    return render_template("index.html")

@app.route("/?<msg>")
def root2(msg):
    return render_template("index.html")




########################################################################################
################################ Register users ########################################
#The method is not allowed for the requested URL. [method POST!]
@app.route("/register", methods=["GET", "POST"])
def register():
    return redirect(url_for('users'))


@app.route("/users", methods=["GET", "POST"])
def users():
    #print(User.query.get(1))

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 8))
    paginate = User.query.paginate(page,
                                     per_page,
                                     error_out=True)
    items = paginate.items

    return render_template("users.html", 
                            paginate=paginate,
                            items=items)


@app.route("/submit_register_users", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        id = request.form.get("id")
        
    if request.method == "GET":
        username = request.args.get("username")
        email = request.args.get("email")
        id = request.args.get("id")
 
    tmp = User(username=username, email=email, id=id ) 
    db.session.add(tmp)
    db.session.commit()

    return redirect(url_for('users'))


@app.route("/BackHome", methods=["GET", "POST"])
def back2home():
    return redirect(url_for("root"))
########################################################################################
########################################################################################


@app.route("/submit_database_choice", methods=["GET", "POST"])
def submit_db():
    if request.method == "POST":
        name = request.form.get("Database")
        age = request.form.get("username")
        _id = request.form.get("password")
        
    if request.method == "GET":
        name = request.args.get("Database")
        age = request.args.get("username")
        _id = request.args.get("password")

    tes = Database("Bilibili")
    #print("Database has tables as following!")
    sql = tes.execute("show table status;")
    #sql = tes.execute("SELECT * FROM User_basic")
    #sql="Bilibili"
    #print(sql)
    print("Database Connected!\n") 
    return render_template("index.html", msg=sql)














########################################################
#################### Table #############################
########################################################################################################################################################################

# Links table
@app.route("/medialink", methods=["GET", "POST"])
def media_link():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM media_link")
    return render_template("links_table.html", 
                           name="media", 
                           results1=results,
                        )
@app.route("/userlink", methods=["GET", "POST"])
def user_link():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM user_link")
    return render_template("links_table.html", 
                           name2="user", 
                           results2=results,
                        )
@app.route("/videolink", methods=["GET", "POST"])
def video_link():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM video_link")
    return render_template("links_table.html", 
                           name3="video", 
                           results3=results,
                        )

########################################################################################################################################################################






############### Basic ##############
@app.route("/Video_basic", methods=["GET", "POST"])
def Video_basic():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM Video_basic")
    return render_template("basic_table.html", 
                           name="Video_basic", 
                           results1=results,
                        )
'''
@app.route("/Video_basic/?<path:msg>", methods=["GET", "POST"])
def Video_basic2(msg):
    #print(msg[0])
    #msg = urllib.unquote(msg)
    #msg.encode(encoding="utf-8")
    #print(type(msg))       

    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM Video_basic")
    return render_template("basic_table.html", 
                           name="Video_basic", 
                           results1=results,
                           #msg=msg
                        )
'''




@app.route("/Article_DataItem", methods=["GET", "POST"])
def Article_DataItem():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM Article_DataItem")
    return render_template("basic_table.html",
                            name2=True, 
                            results2=results
                        )

@app.route("/User_basic", methods=["GET", "POST"])
def User_basic():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM User_basic")
    return render_template("basic_table.html",
                            name3=True, 
                            results3=results
                        )

@app.route("/Anime_DataItem", methods=["GET", "POST"])
def Anime_DataItem():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM Anime_DataItem")
    return render_template("basic_table.html",
                            name4=True, 
                            results4=results
                        )

@app.route("/Partitions", methods=["GET", "POST"])
def Partitions():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM Partitions")
    return render_template("basic_table.html",
                            name5=True, 
                            results5=results
                        )






#################### Upload ########################
@app.route("/Upload_Article", methods=["GET", "POST"])
def Upload_Article():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM Upload_Article")
    return render_template("upload.html",
                            name=True, 
                            results1=results
                        )

@app.route("/User_Upload", methods=["GET", "POST"])
def User_Upload():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM Upload_Article")
    return render_template("upload.html",
                            name2=True, 
                            results2=results
                        )

@app.route("/Upload_Video", methods=["GET", "POST"])
def Upload_Video():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM Upload_Article")
    return render_template("upload.html",
                            name3=True, 
                            results3=results
                        )







#################### Comment ##########################
@app.route("/Barrage", methods=["GET", "POST"])
def Barrage():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM Barrage")
    return render_template("comment.html",
                            name=True, 
                            results1=results
                        )

@app.route("/Comment_on_Anime", methods=["GET", "POST"])
def Comment_on_Anime():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM Comment_on_Anime")
    return render_template("comment.html",
                            name2=True, 
                            results2=results
                        )

@app.route("/Comment_on_Video", methods=["GET", "POST"])
def Comment_on_Video():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM Comment_on_Video")
    return render_template("comment.html",
                            name3=True, 
                            results3=results
                        )

@app.route("/Video_popularity", methods=["GET", "POST"])
def Video_popularity():
    sql = Database('Bilibili')
    results = sql.execute("SELECT * FROM Video_popularity")
    return render_template("comment.html",
                            name4=True, 
                            results4=results
                        )






#################### Other Tables ####################
@app.route("/whatsup", methods=["GET", "POST"])
def whatsup():
    return render_template("index.html")



#################### About ###########################
@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")

























#######################################################################
############################# Video_basic  ##################################
#######################################################################

@app.route("/submit_Video_basic", methods=["GET", "POST"])
def submit_Video_basic():
    if request.method == "POST":
        BVID = request.form.get("BVID")
        title = request.form.get("title")
        videos = request.form.get("videos")
        data = request.form.get("Tag_partition")
        data2 = request.form.get("duration")

    if request.method == "GET":
        BVID = request.args.get("BVID")
        title = request.args.get("title")
        videos = request.args.get("videos")
        data = request.args.get("Tag_partition")
        data2 = request.args.get("duration")
 
    dab = Database("Bilibili")
    sql = dab.execute("INSERT INTO Video_basic (`BVID`, `title`, `videos`, `Tag_partition`, `duration`) VALUES('%s', '%s', %s, '%s', %s);" % (BVID, title, videos, data, data2))
    return redirect(url_for('Video_basic'))

@app.route("/del_Video_basic", methods=["GET", "POST"])
def del_Video_basic():
    if request.method == "POST":
        BVID = request.form.get("BVID")
        
    if request.method == "GET":
        BVID = request.args.get("BVID")
 
    dab = Database("Bilibili")
    sql = dab.execute("DELETE FROM Video_basic WHERE BVID = '%s';" % BVID)
    return redirect(url_for('Video_basic'))

@app.route("/q_Video_basic/", methods=["GET", "POST"])
def q_Video_basic():
    if request.method == "POST":
        BVID = request.form.get("BVID")
        title = request.form.get("title")
        videos = request.form.get("videos")
        data = request.form.get("Tag_partition")
        data2 = request.form.get("duration")

    if request.method == "GET":
        BVID = request.args.get("BVID")
        title = request.args.get("title")
        videos = request.args.get("videos")
        data = request.args.get("Tag_partition")
        data2 = request.args.get("duration")
 
    dab = Database("Bilibili")
    sql = dab.execute("SELECT * FROM Video_basic WHERE title LIKE '%{}%';".format(title))
    
    #return redirect(url_for("Video_basic2", msg=sql))
    # can not solve the problem: 
    # url coding makes unicode str instead of list
    return render_template("query.html", msg=sql)

@app.route("/Back2Previous", methods=["GET", "POST"])
def back2previous():
    return redirect(url_for("Video_basic"))


@app.route("/new_Video_basic", methods=["GET", "POST"])
def new_Video_basic():
    if request.method == "POST":
        BVID = request.form.get("BVID")
        title = request.form.get("title")
        videos = request.form.get("videos")
        data = request.form.get("Tag_partition")
        data2 = request.form.get("duration")

    if request.method == "GET":
        BVID = request.args.get("BVID")
        title = request.args.get("title")
        videos = request.args.get("videos")
        data = request.args.get("Tag_partition")
        data2 = request.args.get("duration")
 
    dab = Database("Bilibili")
    sql = dab.execute("UPDATE Video_basic SET title='%s', videos=%s, Tag_partition='%s', duration=%s WHERE BVID='%s';" % (title, videos, data, data2, BVID))
    return redirect(url_for('Video_basic'))

#######
############################























#######################################################################
############################# User_basic  ##################################
#######################################################################

@app.route("/submit_User_basic", methods=["GET", "POST"])
def submit_User_basic():
    if request.method == "POST":
        data = request.form.get("UP_UID")
        data2 = request.form.get("nickname")
        data3 = request.form.get("sex")
        data4 = request.form.get("PersonSign")
        data5 = request.form.get("levels")
        data6 = request.form.get("coin")
        data7 = request.form.get("Vtype")
 
    dab = Database("Bilibili")
    sql = dab.execute("INSERT INTO User_basic (`UP_UID`, `nickname`, `sex`, `PersonSign`, `levels`, `coin`, `Vtype`) VALUES('%s', '%s', '%s', '%s', %s, %s, %s);" % (data, data2, data3, data4, data5, data6, data7))
    return redirect(url_for('User_basic'))

#######
############################




@app.route("/submit_Article_DataItem", methods=["GET", "POST"])
def submit_Article_DataItem():
    if request.method == "POST":
        data = request.form.get("CVID")
        data2 = request.form.get("title")
        data3 = request.form.get("view")
        data4 = request.form.get("likes")
        data5 = request.form.get("reply_num")
        data6 = request.form.get("tags")
 
    dab = Database("Bilibili")
    sql = dab.execute("INSERT INTO Article_DataItem (`CVID`, `title`, `view`, `likes`, `reply_num`, `tags`) VALUES('%s', '%s', %s, %s, %s, '%s');" % (data, data2, data3, data4, data5, data6))
    return redirect(url_for('Article_DataItem'))

@app.route("/submit_Anime_DataItem", methods=["GET", "POST"])
def submit_Anime_DataItem():
    if request.method == "POST":
        data = request.form.get("media_id")
        data2 = request.form.get("title")
        data3 = request.form.get("Rating")
        data4 = request.form.get("Long_comment")
        data5 = request.form.get("Short_comment")
        data6 = request.form.get("play")
        data7 = request.form.get("follow")
        data8 = request.form.get("barrage")
        data9 = request.form.get("tags")
 
    dab = Database("Bilibili")
    sql = dab.execute("INSERT INTO Anime_DataItem (`media_id`, `title`, `Rating`, `Long_comment`, `Short_comment`, `play`, `follow`, `barrage`, `tags`) VALUES('%s', '%s', %s, %s, %s, %s, %s, %s, '%s');" % (data, data2, data3, data4, data5, data6, data7, data8, data9))
    return redirect(url_for('Anime_DataItem'))

@app.route("/submit_Partitions", methods=["GET", "POST"])
def submit_Partitions():
    if request.method == "POST":
        data = request.form.get("Part_id")
        data2 = request.form.get("Big_partition")
        data3 = request.form.get("Tag_partition")
 
    dab = Database("Bilibili")
    sql = dab.execute("INSERT INTO Partitions (`Part_id`, `Big_partition`, `Tag_partition`) VALUES(%s, '%s', '%s');" % (data, data2, data3))
    return redirect(url_for('Partitions'))





@app.route("/submit_Upload_Article", methods=["GET", "POST"])
def submit_Upload_Article():
    if request.method == "POST":
        data = request.form.get("CVID")
        data2 = request.form.get("UP_UID")
        data3 = request.form.get("pubtime")
 
    dab = Database("Bilibili")
    sql = dab.execute("INSERT INTO Upload_Article (`CVID`, `UP_UID`, `pubtime`) VALUES('%s', '%s', '%s');" % (data, data2, data3))
    return redirect(url_for('Upload_Article'))

@app.route("/submit_User_Upload", methods=["GET", "POST"])
def submit_User_Upload():
    if request.method == "POST":
        data = request.form.get("UP_UID")
        data2 = request.form.get("video")
        data3 = request.form.get("audio")
        data4 = request.form.get("article")
        data5 = request.form.get("album")
 
    dab = Database("Bilibili")
    sql = dab.execute("INSERT INTO User_Upload (`UP_UID`, `video`, `audio`, `article`, `album`) VALUES('%s', %s, %s, %s, %s);" % (data, data2, data3, data4, data5))
    return redirect(url_for('User_Upload'))

@app.route("/submit_Upload_Video", methods=["GET", "POST"])
def submit_Upload_Video():
    if request.method == "POST":
        data = request.form.get("UP_UID")
        data2 = request.form.get("BVID")
        data3 = request.form.get("pubdate")
        data4 = request.form.get("ctime")
 
    dab = Database("Bilibili")
    sql = dab.execute("INSERT INTO Upload_Video (`UP_UID`, `BVID`, `pubdate`, `ctime`) VALUES('%s', '%s', '%s', '%s');" % (data, data2, data3, data4))
    return redirect(url_for('Upload_Video'))




@app.route("/submit_Barrage", methods=["GET", "POST"])
def submit_Barrage():
    if request.method == "POST":
        data = request.form.get("BVID")
        data2 = request.form.get("Time_in_video")
        data3 = request.form.get("Mode")
        data4 = request.form.get("Font_size")
        data5 = request.form.get("Color")
        data6 = request.form.get("Release_date")
        data7 = request.form.get("UP_UID")
        data8 = request.form.get("Dtext")
 
    dab = Database("Bilibili")
    sql = dab.execute("INSERT INTO Barrage (`BVID`, `Time_in_video`, `Mode`, `Font_size`, `Color`, `Release_date`, `UP_UID`, `Dtext`) VALUES('%s', %s, %s, %s, '%s', '%s', '%s', '%s');" % (data, data2, data3, data4, data5, data6, data7, data8))
    return redirect(url_for('Barrage'))

@app.route("/submit_Comment_on_Anime", methods=["GET", "POST"])
def submit_Comment_on_Anime():
    if request.method == "POST":
        data = request.form.get("review_id")
        data2 = request.form.get("article_id")
        data3 = request.form.get("media_id")
        data4 = request.form.get("UP_UID")
        data5 = request.form.get("Size")
        data6 = request.form.get("Rating")
        data7 = request.form.get("title")
        data8 = request.form.get("article")
        data9 = request.form.get("ptime")
 
    dab = Database("Bilibili")
    sql = dab.execute("INSERT INTO Comment_on_Anime (`review_id`, `article_id`, `media_id`, `UP_UID`, `Size`, `Rating`, `title`, `article`, `ptime`) VALUES('%s', '%s', '%s', '%s', %s, %s, '%s', '%s', '%s');" % (data, data2, data3, data4, data5, data6, data7, data8, data9))
    return redirect(url_for('Comment_on_Anime'))

@app.route("/submit_Comment_on_Video", methods=["GET", "POST"])
def submit_Comment_on_Video():
    if request.method == "POST":
        data = request.form.get("Rid")
        data2 = request.form.get("BVID")
        data3 = request.form.get("UP_UID")
        data4 = request.form.get("Ctext")
        data5 = request.form.get("ctime")
        data6 = request.form.get("likes")
        data7 = request.form.get("reply_num")
        data8 = request.form.get("Is_reply")
        data9 = request.form.get("reply_id")
 
    dab = Database("Bilibili")
    sql = dab.execute("INSERT INTO Comment_on_Video (`Rid`, `BVID`, `UP_UID`, `Ctext`, `ctime`, `likes`, `reply_num`, `Is_reply`, `reply_id`) VALUES('%s', '%s', '%s', '%s', '%s', %s, %s, %s, '%s');" % (data, data2, data3, data4, data5, data6, data7, data8, data9))
    return redirect(url_for('Comment_on_Video'))

@app.route("/submit_Video_popularity", methods=["GET", "POST"])
def submit_Video_popularity():
    if request.method == "POST":
        data = request.form.get("BVID")
        data2 = request.form.get("view")
        data3 = request.form.get("barrages")
        data4 = request.form.get("reply")
        data5 = request.form.get("favorite")
        data6 = request.form.get("coin")
        data7 = request.form.get("share")
        data8 = request.form.get("likes")
 
    dab = Database("Bilibili")
    sql = dab.execute("INSERT INTO Video_popularity (`BVID`, `view`, `barrages`, `reply`, `favorite`, `coin`, `share`, `likes`) VALUES('%s', %s, %s, %s, %s, %s, %s, %s);" % (data, data2, data3, data4, data5, data6, data7, data8))
    return redirect(url_for('Video_popularity'))



if __name__ == '__main__':

    app.run(debug=True)
    db.create_all()
    #create()
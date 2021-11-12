#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask, render_template, request, redirect, url_for

from flask_bootstrap import Bootstrap

import pymysql

from database_class import Database

app = Flask(__name__)
Bootstrap(app)




'''
@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello World!'
    
@app.route('/gsq')    
def home():
    return render_template('index.html', name=None)
'''



@app.route('/')
def index():
    '''
    con = pymysql.connect(host="127.0.0.1",
                      user="root", 
                      password="", 
                      db="table", 
                      charset='utf8')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM STU")
    results = cursor.fetchall()
    con.close()
    '''
    sql = Database("table")
    results = sql.execute("SELECT * FROM STU")
    return render_template('test.html', name=None, results=results)    



@app.route("/subm", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        _id = request.form.get("id")
    
    if request.method == "GET":
        name = request.args.get("name")
        age = request.args.get("age")
        _id = request.args.get("id")
    
    '''
    con = pymysql.connect(host="127.0.0.1",
                        user="root", 
                        password="", 
                        db="table", 
                        charset='utf8')
    cursor = con.cursor()
    cursor.execute("INSERT INTO STU (`FIRST_NAME`, `AGE`, `ID`) VALUES('%s', %s, %s)" % (name, age, _id))
    con.commit()
    '''
    #con.close()
    sql = Database("table")
    sql.execute("INSERT INTO STU (`FIRST_NAME`, `AGE`, `ID`) VALUES('%s', %s, %s)" % (name, age, _id))


    return redirect(url_for('index'))



if __name__ == '__main__':
    # 操作系统监听所有公网 IP
    app.run(host='0.0.0.0', debug=True)
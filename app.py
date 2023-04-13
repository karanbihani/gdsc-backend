from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import mysql.connector as sql

DATABASE = "gdsc_social_media"

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:bihani123@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()

try:
    con = sql.connect(host = 'localhost', user = 'root', password = 'bihani123', database = "mysql")
    cur = con.cursor()
    pqry = f"create database {DATABASE};use {DATABASE};create table login(id varchar(20) not null primary key, pwd varchar(20) not null);create table msgs(id varchar(20) not null, msg varchar(2000) not null, time datetime default now(), mid MEDIUMINT NOT NULL AUTO_INCREMENT primary key, likes mediumint not null default 0);"
    cur.execute(pqry)
except:
    print(False)

@app.route('/loginpage/<int:i>')
def loginpage(i):
    e = ["", "User Doesn't Exist", "Invalid Password"]
    return render_template("login.html", error = e[i])

@app.route('/loginpage')
def loginpageerror():
    return redirect(url_for("loginpage", i = 0))

@app.route('/login/', methods=['POST'])
def login():
    global ID 
    if request.method == 'POST':
        id = request.form['id']
        pwd = request.form['pwd']
        
        con = sql.connect(host = 'localhost', user = 'root', password = 'bihani123', database = DATABASE)
        cur = con.cursor()

        pqry = f"select id,pwd from login where id = '{id}';"
        cur.execute(pqry)
        pry = cur.fetchall()

        if pry:
            if pry[0][1] == pwd :
                ID = id
                print(True)
                return redirect(url_for("allmsgs"))
            
            else:
                return redirect(url_for("loginpage", i = 2))
            
        else:
            return redirect(url_for("loginpage", i = 1))

@app.route('/<int:i>')
def signuppage(i = 0):
    e = ["","User Already Exists Try Logging in"]
    return render_template("signup.html", error = e[i])
    
@app.route('/')
def signuperror():
    return redirect(url_for("signuppage", i = 0))

@app.route('/signup/', methods=['POST'])
def signup():
    if request.method == 'POST':
        id = request.form['id']
        pwd = request.form['pwd']

        con = sql.connect(host = 'localhost', user = 'root', password = 'bihani123', database = DATABASE)
        cur = con.cursor()

        pqry = f"select id,pwd from login where id = '{id}';"
        cur.execute(pqry)
        pry = cur.fetchall()
        
        if pry:
            return redirect(url_for("signuppage", i= 1))
        
        q = (f'insert into login (id,pwd) values("{id}", "{pwd}");')
        cur.execute(q)
        con.commit()
        return redirect(url_for("loginpage", i = 0))

@app.route('/mainpage/')
def allmsgs():
    con = sql.connect(host = 'localhost', user = 'root', password = 'bihani123', database = DATABASE)
    cur = con.cursor()

    pqry = f"select id,msg,time,mid,likes from msgs where time > now() - interval 24 hour; sort by time desc"
    cur.execute(pqry)
    all_data = cur.fetchall()
    return render_template("allmsgs.html", data = all_data)

@app.route('/yourpage/')
def yourpage():
    con = sql.connect(host = 'localhost', user = 'root', password = 'bihani123', database = DATABASE)
    cur = con.cursor()

    pqry = f"select id,msg,time,mid,likes from msgs where time > now() - interval 24 hour and (id='{ID}');"
    cur.execute(pqry)
    your_data = cur.fetchall()
    return render_template("yourmsgs.html", data = your_data)

@app.route('/newmessage/')
def newMsg():
    return render_template("newmsg.html")

@app.route('/insert/', methods=['POST'])
def insert():
    if request.method == 'POST':
        msg = request.form['msg']
        id = ID

        con = sql.connect(host = 'localhost', user = 'root', password = 'bihani123', database = DATABASE)
        cur = con.cursor()
        pqry = f'insert into msgs (id, msg) values("{id}","{msg}");'
        cur.execute(pqry)
        con.commit()

    return redirect(url_for("yourpage"))

@app.route('/editmsg/<int:mid>/')
def editmsg(mid):
    con = sql.connect(host = 'localhost', user = 'root', password = 'bihani123', database = DATABASE)
    cur = con.cursor()

    pqry = f"select msg,mid from msgs where (mid={mid}) and (id = '{ID}') ;"
    cur.execute(pqry)
    my_data = cur.fetchall()
    return render_template("editmsg.html", my_data = my_data)

@app.route('/update', methods=['GET','POST'])
def update():
    
    mid = request.form['mid']
    msg = request.form['msg']
    
    if request.method == 'POST':
        con = sql.connect(host = 'localhost', user = 'root', password = 'bihani123', database = DATABASE)
        cur = con.cursor()

        pqry = f"UPDATE msgs SET msg = '{msg}', time = now() WHERE mid={mid} ;"
        cur.execute(pqry)
        con.commit()

    return redirect(url_for("yourpage"))

@app.route('/delete/<mid>/', methods = ["GET", "POST"])
def delete(mid):
    con = sql.connect(host = 'localhost', user = 'root', password = 'bihani123', database = DATABASE)
    cur = con.cursor()
    pqry = f'delete from msgs where mid = {mid};'
    cur.execute(pqry)
    con.commit()
    
    return redirect(url_for("yourpage"))

if __name__ == "__main__":
    app.run(debug = True)
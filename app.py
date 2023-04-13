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
    pqry = f"create database {DATABASE};use {DATABASE};create table login(id varchar(20) not null primary key, pwd varchar(20) not null);create table msgs(id varchar(20) not null, msg varchar(2000) not null, time datetime default now());"
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
                print(True)
                return redirect(url_for("index"))
            
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

if __name__ == "__main__":
    app.run(debug = True)
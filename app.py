from contextlib import nullcontext
from flask import Flask, render_template, request, redirect ,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import *



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'
db= SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# db= SQLAlchemy(app)
class User(db.Model):
    userid = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(80),nullable=False)
   
    def __repr__(self) -> str:
        return f"{self.email} - {self.password}"

        # To Create Tabels in the database file(project.db) in the instance folder
        # write this commands in the terminal
        # 1.python
        # 2.from app import app
        # 3.from app import db
        # 4.db.create_all()
@app.route('/')
def login():
    return render_template("login.html")

@app.route('/checklogin', methods= ['GET','POST'])
def checklogin():
    global user
    if request.method == "POST":
        email1= request.form['email']
        password1= request.form['password']
        rows = User.query.filter_by(email=email1,password=password1).first()
        print(email1)
        print(password1)
        print(rows)
    # allRows = Todo.query.all()
        if (rows)== None:
            return render_template("login.html",rows=rows)
        elif (rows)!= nullcontext:
            session['user']=email1
            return redirect("/dashboard")
        else:
            return redirect("/signup")

@app.route("/signup", methods =['GET','POST'])
def signup():
    if request.method == "POST":
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        newUser = User(username=username, email= email, password=password)
        db.session.add(newUser)
        db.session.commit()
        User.query.all()
        return redirect("/")
    return render_template("signup.html")   

@app.route('/dashboard', methods=['GET','POST'])
# @login_required
def dashboard():
    if session.get('user') == None:
        return redirect("/")
        # print("@@"+session.get('user'))
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)
    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user',None)
    return redirect("/")

@app.route('/about')
def about():
    return render_template("about.html") 

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method =='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/dashboard")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo) 

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/dashboard")  

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template,request, session
from flask_session import Session
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app=Flask(__name__)

engine=create_engine(os.getenv("DATABASE_URL"))
db =scoped_session(sessionmaker(bind=engine))


app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)


@app.route("/",methods=["GET","POST"])
def index():
    
    #if session.get("notes") is None:
    #    session["notes"]=[]
    if(request.method=="POST"):
        comnt=request.form.get("note")
        #session["notes"].append(comment)
        db.execute("INSERT INTO comments(comment)VALUES(:comment)",{"comment":comnt})
    comments=db.execute("SELECT * FROM comments").fetchall()
    db.commit()
    return render_template("index.html",notes=comments)
   
@app.route("/add")
def add():
    return render_template("add.html")
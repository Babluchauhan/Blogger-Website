from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()
app=Flask(__name__)
app.secret_key='super secret key'
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:@localhost/blog"
db.init_app(app) # try "pip install mysqlclient" if showing : no module named mysqldb

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_num = db.Column(db.Integer, nullable=False)
    msg = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=True)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=True)

@app.route("/")
def home():
    posts=Posts.query.filter_by().all()
    return render_template('index.html', posts=posts)

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if ('user' in session and session['user']=='bablu_926'):
        posts=Posts.query.filter_by().all()
        return render_template('dashboard.html', posts=posts)
    
    if (request.method=='POST'):
        user_name=request.form.get('uname')
        user_password=request.form.get('pass')
        if (user_name=='bablu_926' and user_password=='bablu@926'):
            session['user']= user_name
            posts=Posts.query.filter_by().all()
            return render_template('dashboard.html', posts=posts)
    
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',post=post,slug=post_slug)

@app.route("/add_post/<string:sno>", methods=['GET','POST'])
def add_post(sno):
    if (request.method=="POST"):
        if sno=='0':   
            box_title=request.form.get('title')
            slug=request.form.get('slug')
            content=request.form.get('content')
            date=datetime.now()
            post=Posts(title=box_title, slug=slug,content=content,date=date)
            db.session.add(post)
            db.session.commit()
    post=Posts.query.filter_by(sno=sno).first
    return render_template('add_post.html',post=post,sno=sno)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/edit/<string:sno>", methods=['GET','POST'])
def edit(sno):
    if ('user' in session and session['user']=='bablu_926'):
        if (request.method=="POST"):
            box_title=request.form.get('title')
            slug=request.form.get('slug')
            content=request.form.get('content')
            date=datetime.now()
            
            if (sno=='0'):
                post=Posts(title=box_title, slug=slug,content=content,sno=sno,date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post=Posts.query.filter_by(sno=sno).first()
                post.title=box_title
                post.slug=slug
                post.content=content
                post.date=date
                db.session.commit()
                return redirect('/edit/'+sno)
        post=Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html',post=post,sno=sno)
    
@app.route("/delete/<string:sno>", methods=['GET','POST'])
def delete(sno):
    if ('user' in session and session['user']=='bablu_926'):
        post=Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')

@app.route("/contact", methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')

        entry=Contact(name=name, email=email, phone_num=phone, msg=message,date=datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html')


app.run(debug=True)
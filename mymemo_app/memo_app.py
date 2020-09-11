from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_uri = 'mysql+pymysql://root:Kyoto0464#@localhost/memo?charset=utf8'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text())
    content = db.Column(db.Text())

@app.route('/')
def list():
    message = 'My Memo'
    posts = Post.query.all()

    return render_template('list.html', message=message, posts=posts)

@app.route('/show/<int:id>')
def show(id):
    message = 'Memo'+str(id)
    post = Post.query.get(id)

    return render_template('show.html', message=message, post=post)

@app.route('/new')
def new():
    message = 'New Memo'

    return render_template('new.html', message=message)

@app.route('/create', methods=['POST'])
def create():
    message = 'Created Memo'
    new_post = Post()
    new_post.title = request.form['title']
    new_post.content = request.form['content']
    db.session.add(new_post)
    db.session.commit()

    return render_template('show.html', message=message, post=new_post)

@app.route('/destory/<int:id>')
def destory(id):
    message = 'Destoried Memo'+str(id)
    destory_post = Post.query.get(id)
    db.session.delete(destory_post)
    db.session.commit()
    posts = Post.query.all()

    return render_template('list.html', message=message, posts=posts)

@app.route('/edit/<int:id>')
def edit(id):
    message = 'Edit Memo'+str(id)
    post = Post.query.get(id)
    return render_template('edit.html', message=message, post=post)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    message = 'Updated your memo ' + str(id)
    post = Post.query.get(id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()

    return render_template('show.html', message = message, post = post)
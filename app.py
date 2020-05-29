from bottle import Bottle, template, static_file, request, response, redirect
import bottle_session
import bottle_sqlite
import hashlib
from datetime import datetime
from markdown import markdown
from beaker.middleware import SessionMiddleware
from cork import Cork
from cork.backends import SQLiteBackend
import bottle
import os

app = Bottle()
plugin1 = bottle_session.SessionPlugin(cookie_lifetime=600)
app.install(plugin1)
plugin2 = bottle_sqlite.SQLitePlugin(dbfile='./blog.db') 
app.install(plugin2) 
b = SQLiteBackend('blog.db')
aaa = Cork(backend=b)
session_opts = {
	"session.cookie_expires":True,
	"session.encrypt_key":"dardek123",
	"session.httponly":True,
	"session.timeout": 3600*24, 
	"session.type": "cookie",
	"session.validate_key": True
}
app2 = SessionMiddleware(app, session_opts)

#objects of articles, comment, user

class Article():
	def __init__(self, id, date, title, body):
		self.id = id
		self.date = date
		self.title = title
		self.body = body

class Comment():
	def __init__(self, id, user, comment):
		self.id = id
		self.user = user
		self.comment = comment

class User():
	def __init__(self, username, password):
		self.username = username
		self.password = password

def get_articles_database(db):
	return db.execute("SELECT * FROM articles")

def get_articles(db):
	articles_db = get_articles_database(db)
	articles = list()
	for art in articles_db:
		articles.append(Article(art[0], art[1], art[2], art[3]))
	return articles

def get_article_database(db,id):
	return db.execute("SELECT * FROM articles WHERE id=?", (id,))

def get_article(db, id):
	article_db = get_article_database(db,id)
	article = article_db.fetchone()
	return Article(article[0], article[1], article[2], article[3])

def add_article(db, article):
	db.execute("INSERT INTO articles(date, title, body) VALUES (?, ?, ?)", (article.date, article.title, article.body))

def delete_article(db, id):
	db.execute("DELETE FROM articles WHERE id=?", (id,))

def update_article(db, article):
	db.execute("UPDATE articles SET title=?, body=? WHERE id = ?",(article.title, article.body, article.id))

def post_comment(db, comment):
	db.execute("INSERT INTO comments(id, user, comment) VALUES (?, ?, ?)",(comment.id, comment.user, comment.comment))

def get_comments_database(db, id):
	c = db.execute("SELECT * FROM comments WHERE id=?", (id,))
	comments_db = c.fetchall()
	return comments_db

def get_all_comments(db): #debug method
	c = db.execute("SELECT * FROM comments")
	return c.fetchall()

def get_comments(db, id):
	comments_database = get_comments_database(db, id)
	print(get_all_comments(db))
	comments = list()
	for comment in comments_database:
		comments.append(Comment(comment[0], comment[1], comment[2]))
	return comments

def delete_comments_article(db, id):
	db.execute("DELETE FROM comments WHERE id=?", (id,))

@app.get('/upload')
def upload():
	return template('upload')

@app.post('/upload')
def upload():
	upload = request.files.get('upload')
	upload.filename = "pic.png"
	upload.save("./static")

@app.route('/')
def index(session):
	return template('index')

@app.route('/blog')
def index(session,db):
	is_admin = True
	if aaa.user_is_anonymous:
		is_admin = False
	return template('blog', article_list=get_articles(db), admin=is_admin)

@app.route('/static/<filename>')
def server_static(filename):
	return static_file(filename, root='./static')

@app.get('/blog/<id>')
def article(db, id):
	article =  get_article(db, id)
	comments = get_comments(db, id)
	return template('article', id=id, title=article.title, body=markdown(article.body), comments=comments)

@app.post('/blog/<id>')
def comment(db, id):
	comment = request.forms.get('comment')
	comment = Comment(id, "anonymous", comment)
	post_comment(db, comment)
	redirect("/blog/"+str(id))

@app.get('/submit')
def write(session):
	update = False
	aaa.require(role="admin", fail_redirect="/blog")
	return template('submit', update=update)

@app.post('/submit')
def submit(db):
	title = request.forms.get('title')
	body = request.forms.get('body') 
	update = request.forms.get('command')
	article = Article(None, None, title, body)
	if update == "update":
		id = request.forms.get('id')
		article.id = id
		update_article(db, article)
		redirect('/blog')
	else:
		add_article(db, article)
		redirect('/blog')

@app.route('/update/<id>') 
def update(db, session, id):
	article = get_article(db, id)
	if not aaa.user_is_anonymous:
		update = True
		return template("submit", article=article, update=update)

@app.get('/login')
def login_page():
	if aaa.user_is_anonymous:
		return template('login')
	else:
		redirect('/blog') 

@app.post('/login')
def login(db, session):
	username = request.forms.get('username')
	password = request.forms.get('password')
	user = User(username, password)
	try:
		aaa.login(username, password, success_redirect="/blog", fail_redirect="/login")
	except:
		redirect("/login")

@app.route('/logout')
def logout(session):
	aaa.logout(success_redirect="/login")

@app.route('/delete/<id>')
def delete(db, session, id):
	if not aaa.user_is_anonymous:
		delete_article(db, id)
		delete_comments_article(db, id)
	redirect('/blog')	

if __name__ == "__main__":
	if os.environ.get('APP_LOCATION') == 'heroku':
		bottle.run(app=app2,host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
	else:
		bottle.run(app=app2, debug=True, reloader=True)

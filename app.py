from flask import Flask
from flask import render_template, url_for, request, session, redirect
from models.user import User
from models.tag import Tag
from models.bookmark import Bookmark
import models.database as database

app = Flask(__name__)
app.secret_key = "wacky potato fingers"

@app.route("/welcome")
def welcome():
    if 'user_id' in session:
        return redirect(url_for('home'))
    d = { 'logged_in' : False }
    return render_template("welcome.html", d=d)

@app.route("/", methods=["GET", "POST"])
def home():
    if 'user_id' not in session:
        return redirect(url_for("welcome"))

    d = {}
    d['logged_in'] = True
    d['user'] = User(session['user_id'])
    for tag in d['user'].tags:
        print tag.name
    for bookmark in d['user'].untagged:
        print bookmark
    return render_template("home.html", d=d)

@app.route("/login", methods=["POST"])
def login():
    # TODO add id verification
    if 'user_id' not in request.form:
        return redirect(url_for('welcome'))

    session['user_id'] = request.form['user_id']
    user = User(session['user_id'])
    if user.username:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('register'))

@app.route("/register", methods=["GET","POST"])
def register():
    if 'user_id' not in session:
        return redirect(url_for('welcome'))
    if request.method == "GET":
        d = { 'logged_in' : False }
        return render_template("register.html", d=d, repeat='False')

    user = User(session['user_id'])
    if not user.setUsername(request.form['usern']):
        d = { 'logged_in' : False }
        return render_template("register.html", d=d, repeat='True')
    b = Bookmark("Google", "http://google.com")
    b.creator = user.user_id
    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    if 'user_id' in session:
        del session['user_id']
    return redirect(url_for('home'))

@app.route("/action", methods=["POST"])
def action():
    if 'action' not in request.form:
        return "error: no action"

    action = request.form['action']
    if action == 'make-bookmark':
        b = Bookmark(request.form['title'], request.form['link'])
        b.creator = request.form['user_id']
        print "make-bookmark %s %s"%(request.form['title'], request.form['link'])
        return str(b.idnum)
    elif action == 'remove-bookmark':
        database.removeBookmark(request.form['bookmark_id'])
        print "remove-bookmark %s"%request.form['bookmark_id']
        return "Bookmark removed"
    elif action == 'make-tag':
        u = User(request.form['user_id'])
        t = Tag(request.form['tag_name'])
        t.creator = u.user_id
        u.tags.append(t)
        print "make-tag %s %s: %s"%(request.form['user_id'], request.form['tag_name'],
                                    t.idnum)
        return str(t.idnum)
    elif action == 'add-tag':
        b = Bookmark(idnum=request.form['bookmark_id'])
        t = Tag(idnum=request.form['tag_id'])
        print b.tags
        b.tags.append(t)
        t.bookmarks.append(b)
        b.unload()
        t.unload()
        print "add-tag", request.form['bookmark_id'], request.form['tag_id']
        return "tagging added"

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

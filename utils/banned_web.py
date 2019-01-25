from utils.db import db
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def banned():
    # users = {}
    curs = db.cursor()
    res = curs.execute("select username, count from users join bans").fetchall()
    return render_template("banned.html", users=res)

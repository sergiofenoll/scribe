from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

@app.route('/')
def banned():
    with sqlite3.connect("messages.db") as con:
        cur = con.cursor()
        return render_template("banned.html", users=cur.execute("select username, count from users join bans on users.u_id=bans.u_id where users.end_time='9999-12-31 00:00:00' and bans.g_id=140942235670675456 order by count desc").fetchall())

if __name__ == "__main__":
    app.run()

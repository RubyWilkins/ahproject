from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route ("/movements")
def movements ():
    conn = sqlite3.connect("Art.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Movements")
    results = cur.fetchall()
    return render_template("all_movements.html", results = results)

@app.route ("/movement/<int:id>")
def movement (id):
    conn = sqlite3.connect("Art.db")
    cur = conn.cursor()
    cur.execute("SELECT name,desc FROM Movements WHERE id=?",(id,))
    mov = cur.fetchone()
    cur.execute("SELECT name, image FROM Work WHERE mid=?",(id,))
    works = cur.fetchall()
    return render_template("movement.html", movement=mov, works=works)

@app.route ("/work/<int:id>")
def work (id):
    conn = sqlite3.connect("Art.db")
    cur = conn.cursor()
    cur.execute("SELECT name,desc,image, rid FROM Work WHERE id=?",(id,))
    work = cur.fetchone()
    cur.execute("SELECT name, desc FROM Artist WHERE id=?",(work[3],))
    artist = cur.fetchone()
    return render_template("work.html",work=work, artist=artist)

if __name__ == "__main__":
    app.run(debug=True)

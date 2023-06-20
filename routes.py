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
    cur.execute("SELECT name,description FROM Movements WHERE id=?",(id,))
    mov = cur.fetchone()
    cur.execute("SELECT aid, name FROM Work WHERE mid=?",(id,))
    works = cur.fetchall()
    print(mov)
    print(works)
    return render_template("movement.html", name=mov[0] , description=mov[1], results=works)

@app.route ("/work/<int:id>")
def work (id):
    conn = sqlite3.connect("Art.db")
    cur = conn. cursor()
    cur.execute("SELECT name, description FROM Work WHERE aid=?",(id,))
    work = cur.fetchone()
    print("Hello World",work)
    return render_template ("movement.html", name=work[0], description=work[1])

if __name__ == "__main__":
    app.run(debug=True)

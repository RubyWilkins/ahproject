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

#this code shows all the movements

@app.route ("/movements")
def movements ():
    conn = sqlite3.connect("Art.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Movements")
    results = cur.fetchall()
    return render_template("all_movements.html", results = results)

#this displays the artworks in a movement

@app.route ("/movement/<int:id>")
def movement (id):
    conn = sqlite3.connect("Art.db")
    cur = conn.cursor()
    cur.execute("SELECT name,description FROM Movements WHERE id=?",(id,))
    mov = cur.fetchone()
    cur.execute("SELECT aid, name, image FROM Work WHERE mid=?",(id,))
    works = cur.fetchall()
    print(mov)
    print(works)
    return render_template("movement.html", name=mov[0] , description=mov[1], results=works)

#this code displays the artwork

@app.route ("/work/<int:id>")
def work (id):
    conn = sqlite3.connect("Art.db")
    cur = conn. cursor()
    cur.execute("SELECT name, description FROM Work WHERE aid=?",(id,))
    work = cur.fetchone()
    print("Hello World",work)
    return render_template ("movement.html", name=work[0], description=work[1])

#this is the code for the search 


from flask import request

@app.route("/search/<string:strings>")
def search(strings=None):
    if strings is None:
        strings = ""

    conn = sqlite3.connect("Art.db")
    cur = conn.cursor()

    # Use a parameterized query to avoid SQL injection
    cur.execute(f"SELECT name FROM Work WHERE name LIKE ?", ('%' + strings + '%',))

    results = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("search.html", search_query=strings, results=results)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)

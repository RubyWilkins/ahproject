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

from flask import request

@app.route("/search/")
@app.route("/search/<string:search_query>")
def search(search_query=None):
    if search_query is None:
        search_query = ""

    conn = sqlite3.connect("Art.db")
    cur = conn.cursor()

    # Use a parameterized query to avoid SQL injection
    cur.execute(f"SELECT name FROM Work WHERE name LIKE ?", ('%' + search_query + '%',))

    # Fetch all the results from the query
    results = cur.fetchall()

    # Close the cursor and the database connection
    cur.close()
    conn.close()

    return render_template("search.html", search_query=search_query, results=results)




if __name__ == "__main__":
    app.run(debug=True)

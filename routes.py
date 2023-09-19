import sqlite3
from flask import Flask, render_template
from flask import request

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


# this code shows all the movements
@app.route("/movements")
def movements():
    conn = sqlite3.connect("Art.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Movements")
    results = cur.fetchall()
    return render_template("all_movements.html", results=results)


# this displays the all of artworks in a specific movement
@app.route("/movement/<int:id>")
def movement(id):
    conn = sqlite3.connect("Art.db")
    cur = conn.cursor()
    # the id is specifying which movement
    cur.execute("SELECT name, description FROM Movements WHERE id=?", (id,))
    mov = cur.fetchone()
    # if the mid doesn't exist return 404
    if not mov:
        return render_template('404.html')
    # the mid is the movement id
    cur.execute("SELECT aid, name, image FROM Work WHERE mid=?", (id,))
    works = cur.fetchall()
    # if there were no works for this movement works will be [] which isn't an error
    return render_template("movement.html", name=mov[0], description=mov[1], results=works)


# this code displays the artwork
@app.route("/work/<int:id>")
def work(id):
    conn = sqlite3.connect("Art.db")
    cur = conn.cursor()
    # the aid is the artwork's id
    cur.execute("SELECT name, description,image FROM Work WHERE aid=?", (id,))
    work = cur.fetchone()
    # if the aid doesn't exist return 404
    if not work:
        return render_template('404.html')
    return render_template("work.html", name=work[0], description=work[1], item=work[2])


# this is the code for the artists
@app.route("/artists")
def artists():
    conn = sqlite3.connect("Art.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM Artist")
    results = cur.fetchall()
    return render_template("all_artists.html", results=results)


# this displays all of the artworks for a specific artist
@app.route("/artist/<int:id>")
def artist(id):
    conn = sqlite3.connect("Art.db")
    cur = conn.cursor()
    # the id is specifying which artist
    cur.execute("SELECT name, description FROM Artist WHERE id=?", (id,))
    artist = cur.fetchone()
    # if the aid doesn't exist return 404
    if not artist:
        return render_template('404.html')
    # the rid is the artist id
    cur.execute("SELECT aid, name, image FROM Work WHERE rid=?", (id,))
    works = cur.fetchall()
    # if there were no works for this artist works will be [] which isn't an error
    return render_template("artist.html", name=artist[0], description=artist[1], results=works)


# this is the code for the search
@app.route("/search")
def search():
    query = request.args.get('query', type=str)

    if not query:
        return render_template("home.html")

    conn = sqlite3.connect("Art.db")
    cur = conn.cursor()

    # Use a parameterized query to avoid SQL injection
    cur.execute("SELECT aid, name FROM Work WHERE name LIKE ?", ('%' + query + '%',))
    wresults = cur.fetchall()

    cur.execute("SELECT aid, name FROM Work WHERE rid IN \
                (SELECT id FROM Artist WHERE name LIKE ?)",
                ('%' + query + '%',))
    aresults = cur.fetchall()
    results = wresults + aresults

    # there can be duplicates because a work can appear in wresults and
    # aresults, so i added this to remove them
    results = list(set(results))

    cur.close()
    conn.close()

    return render_template("search.html", search_query=query, results=results)


# this is the code for the 404 page, so the website doesn't break if anyone types something weird in the url bar thing
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == "__main__":
    # listen on all interfaces so I can connect from my phone to test the grid
    app.run(debug=True, host='0.0.0.0')

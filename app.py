from flask import Flask, request, render_template, jsonify
from wtforms import TextAreaField, TextField, StringField, SubmitField, validators
import sqlite3

app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/',)
def api_list_welcome():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_prod = cur.execute('SELECT PRODUCT FROM REVIEWS;').fetchall()

    return render_template('index.html', all_prod = all_prod)

@app.route('/add', methods = ['GET', 'POST'])
def addRev():
    if request.method == 'POST':
        try:
            nm = request.form['name']
            prod = request.form['prod']
            rev = request.form['rev']
            rate = request.form['rate']
            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO REVIEWS (Name, Product, Review, Rating) VALUES (?,?,?,?)", (nm, prod, rev, rate))
                conn.commit()
                msg = "Review Addition Successful."
        except:
            conn.rollback()
            msg = "Review Addition Failed."
        finally:
            return render_template("rev_result.html", msg = msg)
            conn.close()

@app.route('/review', methods = ['GET'])
def api_rev():
    query_parameters = request.args

    product = query_parameters.get('product')

    query = "SELECT * FROM REVIEWS WHERE"
    to_filter = []

    if product:
        query += ' PRODUCT = ?'
        to_filter.append(product)
    if not product:
        return page_not_found(404)

    query = query + ';'

    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return render_template('rev_result.html', results = results, Product = product)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run(debug = True)
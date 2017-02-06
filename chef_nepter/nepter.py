import csv
import sqlite3
from sqlite3 import Error
import operator
import collections
from flask import Flask, send_from_directory, render_template
from flask_restful import Resource, Api, request



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except Error as e:
        print(e)

    return None

conn = create_connection("nepter_db")

app = Flask(__name__, static_url_path='/static')


@app.route('/get_recipes', methods=['POST'])
def handle_recipes():
    ingredients = []
    for ingredient in request.form:
        if ingredient != 'recipes':
            ingredients.append(ingredient)
    print(ingredients)
    relevant_recipes = get_recipes(conn, ingredients)
    return render_template('recipes.html', recipes=relevant_recipes)


def get_recipes(conn, ingredients):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    sql = "SELECT r.name, ir.ingredient_id, p.perishability from ingredients_to_recipes ir " \
          "left join perishability p on p.ingredient = ir.ingredient_id " \
          "left join recipes r on r.id = ir.recipe_id where ingredient_id in " \
          "(SELECT id FROM ingredients where name in ({seq}))".format(seq=','.join(['?']*len(ingredients)))
    cur.execute(sql, ingredients)
    return cur.fetchall()


def get_ingredients(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT name FROM ingredients")
    ingredients = cur.fetchall()
    ingredients.sort()
    return ingredients


@app.route('/')
def index_page():
    return render_template("index.html", ingredients=get_ingredients(conn))

def main():
    app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    main()

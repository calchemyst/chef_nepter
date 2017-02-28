import collections

import sqlite3
from sqlite3 import Error
from flask import Flask, send_from_directory, render_template
from flask_restful import Resource, Api, request
from recipe import Recipe


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
    relevant_recipes = get_recipes(conn, ingredients)
    return render_template('recipes.html', recipes=relevant_recipes)


def get_recipes(conn, ingredients):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    recipe_results = []
    cur = conn.cursor()
    recipes_relevancy = collections.defaultdict(list)
    for ingredient in ingredients:
        # TODO: Beware sql injection?
        sql = """SELECT r.name, r.location, i.name from ingredients_to_recipes ir
              inner join recipes r on r.id = ir.recipe_id
              inner join ingredients i on i.id = ir.ingredient_id
              where ir.ingredient_id in
                (SELECT id FROM ingredients where name='{0}')""".format(ingredient)
        result_set = cur.execute(sql)
        results = result_set.fetchall()
        for result in results:
            r = Recipe(result[0], result[1])
            recipes_relevancy[r].append(ingredient)
    for r in sorted(recipes_relevancy, key=lambda k: len(recipes_relevancy[k]), reverse=True):
        score = len(recipes_relevancy[r])
        name = r.name
        location = r.location
        recipe_results.append((name, location, score, recipes_relevancy[r]))
    return recipe_results




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


def get_ingredient_names(conn, ingredient_ids):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    sql = """SELECT name FROM ingredients where id in ({seq})""".format(seq=','.join(['?']*len(ingredient_ids)))
    cur.execute(sql, ingredient_ids)
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

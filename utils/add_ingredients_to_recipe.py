import sqlite3
from sqlite3 import Error


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



def add_ingredients_to_recipe(conn, recipe_loc, ingredient_info):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    recipe_sql = """SELECT * FROM recipes WHERE LOCATION = '{0}'""".format(recipe_loc)
    cur.execute(recipe_sql)
    recipe_results = cur.fetchone()
    recipe_id = recipe_results[0]
    if len(recipe_results) == 0:
        print("Recipe needs to be added first.")
    else:
        add_ingredients_to_recipe_id(conn, recipe_id, ingredient_info)



def add_ingredients_to_recipe_id(conn, recipe_id, ingredient_info):
    cur = conn.cursor()
    for ii in ingredient_info:
        quantity = ingredient_info[ii][0]
        unit = ingredient_info[ii][1]
        ingredient_sql = """SELECT * FROM ingredients WHERE NAME = '{0}'""".format(ii)
        cur.execute(ingredient_sql)
        results = cur.fetchone()
        if len(results) == 0:
            print("Need to add this ingredient first")
        else:
            ingredient_id = results[0]
            ingredient_to_recipes_sql = """INSERT INTO ingredients_to_recipes
            (INGREDIENT_ID,RECIPE_ID, QUANITY, UNIT)
             VALUES ({0}, {1}, {2}, {3})""".format(ingredient_id, recipe_id, quantity, unit)
            print(ingredient_to_recipes_sql)

def main():
    add_ingredients_to_recipe(conn, 'https://www.blueapron.com/recipes/south-indian-squash-curry-with-basmati-rice',
                              {'bread': (1,'ea') })

if __name__ == '__main__':
    main()

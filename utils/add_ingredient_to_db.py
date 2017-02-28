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

def add_ingredient(conn, name, perishability, cost, unit):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    sql = """SELECT * FROM ingredients WHERE NAME = '{0}'""".format(name)
    cur.execute(sql)
    results = cur.fetchall()
    if len(results) == 0:
        sql = """SELECT id FROM ingredients ORDER BY id DESC LIMIT 1"""
        cur.execute(sql)
        ingredient_id = cur.fetchone()[0] + 1
        ingredient_sql = """INSERT INTO ingredients (ID,NAME) VALUES ({0}, '{1}')""".format(ingredient_id, name)
        score_sql = """INSERT INTO perishability (INGREDIENT,PERISHABILITY) VALUES ({0}, {1})""".format(ingredient_id, perishability)
        cost_sql = """INSERT INTO ingredients_to_price (ID, PRICE, UNIT) VALUES ({0}, {1}, '{2}')""".format(ingredient_id, cost, unit)
        cur.execute(ingredient_sql)
        cur.execute(score_sql)
        cur.execute(cost_sql)
        conn.commit()
    else:
        print("Already have this ingredient's data!")




def main():
    add_ingredient(conn, 'dates', 365, 600, 'lb')

if __name__ == '__main__':
    main()

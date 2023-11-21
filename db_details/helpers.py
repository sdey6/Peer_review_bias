import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a db_details connection to the SQLite db_details
        specified by db_file
    :param db_file: db_details file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file,timeout=10)
        print("Opened db_details successfully")
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

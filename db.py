# import m
import mysql.connector as m

# database_url = "postgresql://postgres:Av4936754@localhost/postgres"

database_url = {
    'user': 'root',
    'password': 'Av4936754',
    'host': "localhost",
    'database': 'water',
    'port': 3306,
}


def execute_query(query, select=False):
    conn = None
    try:
        conn = m.connect(**database_url)
        cursor = conn.cursor()
        cursor.execute(query)
        if select:
            print(1)
            rows = cursor.fetchall()

        cursor.close()
        conn.commit()
        if select:
            return rows
    except:
        print('Error PostgreSQL')
    finally:
        if conn is not None:
            conn.close()


def registration(login, password):
    # execute_query(f"insert into users (login, password) values ('{login}','{password}')")
    conn = m.connect(**database_url)
    cursor = conn.cursor()
    cursor.execute(f"insert into users (login, password) values ('{login}','{password}')")
    conn.commit()


def auth(login, password):
    user = execute_query(f"select * from users where login = '{login}' and password = '{password}'")
    if user:
        return True
    return False


def check_login(login):
    conn = m.connect(**database_url)
    cursor = conn.cursor()
    cursor.execute("select * from users where login = '" + login + "'")
    if cursor.fetchone():
        return True
    return False


def get_user(login):
    conn = m.connect(**database_url)
    cursor = conn.cursor()
    cursor.execute("select * from users where login = '" + login + "'")
    return cursor.fetchone()


def update_password(password, login):
    conn = m.connect(**database_url)
    cursor = conn.cursor()
    cursor.execute("update users set password = '" + password + "' where login  = '" + login + "'")
    conn.commit()


def get_water_limit(login):
    conn = m.connect(**database_url)
    cursor = conn.cursor()
    cursor.execute("select * from users where login = '" + login + "'")
    return cursor.fetchone()[3]


def get_water_count(login):
    conn = m.connect(**database_url)
    cursor = conn.cursor()
    cursor.execute("select * from users where login = '" + login + "'")
    return cursor.fetchone()[4]


def set_water_count(login, count_water):
    conn = m.connect(**database_url)
    cursor = conn.cursor()
    cursor.execute("update users set count_water = " + count_water + " where login = '" + login + "'")
    conn.commit()


def get_all_water(login):
    conn = m.connect(**database_url)
    cursor = conn.cursor()
    cursor.execute("select * from users where login = '" + login + "'")
    return cursor.fetchone()

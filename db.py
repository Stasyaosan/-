import psycopg2

database_url = "postgresql://postgres:Av4936754@localhost/postgres"


def execute_query(query, select=False):
    conn = None
    try:
        conn = psycopg2.connect(database_url)
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


def reg(login, password):
    execute_query(f"insert into users (login, password) values ('{login}', '{password}')")


def auth(login, password):
    user = execute_query(f"select * from users where login = '{login}' and password = '{password}'")
    if user:
        return True
    return False


def check_login(login):
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    cursor.execute("select * from users where login = '" + login + "'")
    if cursor.fetchone():
        return True
    return False


def get_user(login):
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    cursor.execute("select * from users where login = '" + login + "'")
    return cursor.fetchone()


def update_password(password, login):
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    cursor.execute("update users set password = '" + password + "' where login  = '" + login + "'")
    conn.commit()


def get_water_limit(login):
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    cursor.execute("select * from users where login = '" + login + "'")
    return cursor.fetchone()[3]


def get_water_count(login):
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    cursor.execute("select * from users where login = '" + login + "'")
    return cursor.fetchone()[4]

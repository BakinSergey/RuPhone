import psycopg2

from psycopg2.extras import RealDictCursor
from contextlib import closing

from envparse import env

env.read_envfile()


def connect_db():
    host = env.str('DB_HOST')
    user = env.str('DB_USER')
    password = env.str('DB_PASS')
    db_name = env.str('DB_NAME')

    conn = psycopg2.connect(dbname=db_name, user=user,
                            password=password, host=host,
                            cursor_factory=RealDictCursor
                            )
    return conn


def truncate_phone_table():
    conn = connect_db()
    with closing(conn) as conn:
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE phonedata_phonerange')
        conn.commit()


def insert_csvblob(csv_blob, reestr_url):
    data = [(r[0], r[1], r[2], r[4], r[5],) for r in csv_blob]

    conn = connect_db()
    with closing(conn) as conn:
        cur = conn.cursor()
        try:
            insert_query = "insert into phonedata_phonerange (code, start, finish, provider, region) values %s"
            psycopg2.extras.execute_values(cur, insert_query, data, template=None, page_size=100)
        except:
            print('except was raised')

        finally:
            print(f'reestr {reestr_url.split("/")[-1]} was loaded')
            conn.commit()

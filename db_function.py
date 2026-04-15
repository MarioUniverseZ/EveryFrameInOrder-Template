import pymysql
from config import DB_CONFIG

def get_connection():
    return pymysql.connect(**DB_CONFIG)


def get_next_frames(anime, limit=2):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = f"""
                SELECT *
                FROM {DB_CONFIG['database']}.{anime}
                WHERE post_time IS NULL
                ORDER BY id ASC
                LIMIT {limit}
            """
            cursor.execute(sql,)
            return cursor.fetchall()
    finally:
        pass


def mark_posted(anime, frame_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = f"""
                UPDATE {DB_CONFIG['database']}.{anime}
                SET post_time = NOW()
                WHERE id = {frame_id}
            """
            cursor.execute(sql,)
        conn.commit()
    finally:
        conn.close()
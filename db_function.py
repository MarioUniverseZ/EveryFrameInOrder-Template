import pymysql
from config import DB_CONFIG

def get_connection():
    return pymysql.connect(**DB_CONFIG)


def get_next_frame():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT *
                FROM posted_frames
                WHERE post_time IS NULL
                ORDER BY id ASC
                LIMIT 1
            """
            cursor.execute(sql)
            return cursor.fetchone()
    finally:
        conn.close()


def mark_posted(frame_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE posted_frames
                SET post_time = NOW()
                WHERE id = %s
            """
            cursor.execute(sql, (frame_id,))
        conn.commit()
    finally:
        conn.close()


def get_total_frames_for_episode(episode):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT COUNT(*) as total
                FROM posted_frames
                WHERE episode = %s
            """
            cursor.execute(sql, (episode,))
            return cursor.fetchone()["total"]
    finally:
        conn.close()
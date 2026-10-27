import mysql.connector
from mysql.connector import Error
import streamlit as st

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "NewStrongPass123!",        # <-- Set your MySQL root password here
    "database": "company_management_db",
}


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        st.error(f"Database connection failed: {e}")
        return None


def run_query(sql, params=None, fetch=True):
    conn = get_connection()
    if not conn:
        return [] if fetch else False
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return True
    except Error as e:
        st.error(f"Query error: {e}")
        return [] if fetch else False
    finally:
        conn.close()

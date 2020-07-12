import sqlite3
from sqlite3 import Error

from log import log


def connect_database(db_file):
    log("Attempting to connect to settings database...")
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        log("Database connected")
    except Error as e:
        log(e)
    return conn


def create_table(conn, sql):
    log("Creating settings table...")
    try:
        c = conn.cursor()
        c.execute(sql)
        log("Settings table created")
    except Error as e:
        print(e)


def insert_settings_record(conn, settings):
    sql = """INSERT INTO settings_v1(cmdr,origin,destination)
    VALUES(?,?,?)"""
    log("Inserting new settings record...")
    cur = conn.cursor()
    cur.execute(sql, settings)
    return cur.lastrowid


def update_settings_record(conn, settings):
    sql = """UPDATE settings_v1
    SET origin = ? ,
        destination = ?
    WHERE cmdr = ?"""
    log("Updating existing settings record...")
    cur = conn.cursor()
    cur.execute(sql, settings)
    return cur.lastrowid


def select_settings_records(conn):
    log("Getting settings table")
    cur = conn.cursor()
    cur.execute("SELECT * FROM settings_v1")
    rows = cur.fetchall()
    return rows


def setup(db_file):
    create_settings_table_sql = """CREATE TABLE IF NOT EXISTS settings_v1 (
    cmdr TEXT,
    origin TEXT,
    destination TEXT
    );"""
    log("Starting settings database setup...")
    conn = connect_database(db_file)
    if conn is not None:
        create_table(conn, create_settings_table_sql)
        log("Settings database setup complete")


def update(db_file, cmdr, origin, destination):
    log("Updating settings database...")
    conn = connect_database(db_file)
    if conn is not None:
        settings_table = select_settings_records(conn)
        if cmdr in settings_table:
            update_settings_record(conn, (origin, destination, cmdr))
        else:
            insert_settings_record(conn, (cmdr, origin, destination))
        log("Settings database updated")

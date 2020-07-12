import sqlite3
from sqlite3 import Error

from log import log


def connect_database(db_file):
    log("Attempting to connect to systems database...")
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        log("Database connected")
    except Error as e:
        log(e)
    return conn


def create_table(conn, sql):
    log("Creating systems table...")
    try:
        c = conn.cursor()
        c.execute(sql)
        log("Systems table created")
    except Error as e:
        print(e)


def insert_systems_record(conn, systems):
    sql = """INSERT INTO systems(cmdr,origin,destination)
    VALUES(?,?,?)"""
    log("Inserting new systems record...")
    cur = conn.cursor()
    cur.execute(sql, systems)
    return cur.lastrowid


def update_systems_record(conn, systems):
    sql = """UPDATE systems
    SET origin = ? ,
        destination = ?
    WHERE cmdr = ?"""
    log("Updating existing systems record...")
    cur = conn.cursor()
    cur.execute(sql, systems)
    return cur.lastrowid


def select_systems_records(conn):
    log("Getting systems table")
    cur = conn.cursor()
    cur.execute("SELECT * FROM systems")
    rows = cur.fetchall()
    return rows


def setup(db_file):
    create_systems_table_sql = """CREATE TABLE IF NOT EXISTS systems (
    cmdr TEXT,
    origin TEXT,
    destination TEXT
    );"""
    log("Starting systems database setup...")
    conn = connect_database(db_file)
    if conn is not None:
        create_table(conn, create_systems_table_sql)
        log("Systems database setup complete")


def update(db_file, cmdr, origin, destination):
    log("Updating systems database...")
    conn = connect_database(db_file)
    if conn is not None:
        systems_table = select_systems_records(conn)
        if cmdr in systems_table:
            update_systems_record(conn, (origin, destination, cmdr))
        else:
            insert_systems_record(conn, (cmdr, origin, destination))
        log("Systems database updated")

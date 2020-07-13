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


def insert_systems_record(conn, data):
    sql = """INSERT INTO systems(cmdr,origin,destination)
    VALUES(?,?,?)"""
    log("Inserting new systems record...")
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid


def update_systems_record(conn, data):
    sql = """UPDATE systems
    SET origin = ? ,
        destination = ?
    WHERE cmdr = ?"""
    log("Updating existing systems record...")
    cur = conn.cursor()
    cur.execute(sql, data)
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
    destination TEXT,
    travelled FLOAT
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
        records_amount = len(systems_table)
        records_checked = 0
        for record in systems_table:
            if cmdr in record:
                update_systems_record(conn, (origin, destination, cmdr))
            else:
                records_checked += 1
        if records_checked >= records_amount:
            insert_systems_record(conn, (cmdr, origin, destination))
        log("Systems database updated")


def get_systems(db_file, cmdr):
    log("Retrieving CMDR systems from database...")
    success = False
    origin = ""
    destination = ""
    conn = connect_database(db_file)
    if conn is not None:
        systems_table = select_systems_records(conn)
        records_amount = len(systems_table)
        records_checked = 0
        for record in systems_table:
            if cmdr in record:
                log("Retrieving systems...")
                success = True
                origin = record[1]
                destination = record[2]
                log("Systems retrieval complete")
            else:
                records_checked += 1
        if records_checked >= records_amount:
            log("Failed to retrieve systems, using values stored in registry instead")
            success = False
    return success, origin, destination

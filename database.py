import sqlite3
from sqlite3 import Error

from log import log


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.setup()

    def setup(self):
        create_systems_table_sql = """CREATE TABLE IF NOT EXISTS systems (
        cmdr TEXT,
        origin TEXT,
        destination TEXT,
        travelled FLOAT
        );"""
        log("Starting systems database setup...")
        conn = self.__connect_database()
        if conn is not None:
            self.conn = conn
            self.__create_table(create_systems_table_sql)
            log("Systems database setup complete")

    def update(self, cmdr, origin, destination):
        log("Updating systems database...")
        if self.conn is not None:
            systems_table = self.__select_systems_records()
            records_amount = len(systems_table)
            records_checked = 0
            for record in systems_table:
                if cmdr in record:
                    self.__update_systems_record((origin, destination, cmdr))
                else:
                    records_checked += 1
            if records_checked >= records_amount:
                self.__insert_systems_record((cmdr, origin, destination))
            log("Systems database updated")

    def get_systems(self, cmdr):
        log("Retrieving CMDR systems from database...")
        success = False
        origin = ""
        destination = ""
        if self.conn is not None:
            systems_table = self.__select_systems_records()
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

    def __connect_database(self):
        log("Attempting to connect to systems database...")
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            log("Database connected")
        except Error as e:
            log(e)
        return conn

    def __create_table(self, sql):
        log("Creating systems table...")
        try:
            c = self.conn.cursor()
            c.execute(sql)
            log("Systems table created")
        except Error as e:
            print(e)

    def __insert_systems_record(self, data):
        sql = """INSERT INTO systems(cmdr,origin,destination)
        VALUES(?,?,?)"""
        log("Inserting new systems record...")
        cur = self.conn.cursor()
        cur.execute(sql, data)
        self.conn.commit()
        return cur.lastrowid

    def __update_systems_record(self, data):
        sql = """UPDATE systems
        SET origin = ? ,
            destination = ?
        WHERE cmdr = ?"""
        log("Updating existing systems record...")
        cur = self.conn.cursor()
        cur.execute(sql, data)
        self.conn.commit()
        return cur.lastrowid

    def __select_systems_records(self):
        log("Getting systems table")
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM systems")
        rows = cur.fetchall()
        return rows

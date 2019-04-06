#!/usr/bin/python
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create database connection """
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        conn.close()
 
def create_table(db_file):
    """ create HOSTLIST table in database """
    try:
        conn = sqlite3.connect(db_file)
        conn.execute('''CREATE TABLE IF NOT EXISTS HOSTLIST 
                 (hostid INTEGER PRIMARY KEY AUTOINCREMENT,
                 hostname TEXT NOT NULL,
                 application TEXT NOT NULL,
                 database TEXT NOT NULL);''')
    except Error as e:
        print(e)
    finally:
        conn.commit()
        conn.close()


def listhosts(db_file, name):
    """ Query hosts in HOSTLIST """
    try:
        conn = sqlite3.connect(db_file)
        rows = conn.execute("SELECT * FROM HOSTLIST").fetchall()
        if name == 'ALL':
            for row in rows:
                print(row)
        else:
            for row in rows:
                for entry in row:  
                    if entry == name:
                       print(entry)
                       status = "found"
                       break
                    else:
                       status = "not found"
                if status == "found":
                    break  
            if status == "not found":
                print("Hostname not found")
    except Error as e:
        print(e)
    finally:
        conn.close()


def add_host(db_file, host_name, application_name, database_name):
    """ Add new host to table """
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("INSERT INTO HOSTLIST(hostname,application,database) VALUES(?,?,?)", (host_name, application_name, database_name))
    except Error as e:
        print(e)
    finally:
        conn.commit()
        conn.close()

def delete_host(db_file, host_name, application_name, database_name):
    """ Remove host from table """
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("DELETE FROM HOSTLIST WHERE hostname=?", (host_name,))
    except Error as e:
        print(e)
    finally:
        conn.commit()
        conn.close()

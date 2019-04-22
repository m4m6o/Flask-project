# -*- coding: utf-8 -*-
import sqlite3
import os
 
class DB:
    def __init__(self, db_name):
        conn = sqlite3.connect(os.path.join('db', db_name), check_same_thread=False)
        self.conn = conn
 
    def get_connection(self):
        return self.conn
 
    def __del__(self):
        self.conn.close()

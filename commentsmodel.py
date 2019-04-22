# -*- coding: utf-8 -*-
import sqlite3

class CommentsModel():
    def __init__(self, connection):
        self.connection = connection
        
    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS comments 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             author_id INTEGER,
                             news_id INTEGER,
                             content VARCHAR(100),
                             user VARCHAR(200))''')
        cursor.close()
        self.connection.commit()
        
    def insert(self, author_id, news_id, content, user):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO comments 
                          (author_id, news_id, content, user) 
                          VALUES (?, ?, ?, ?)''', (author_id, news_id, content, user))
        cursor.close()
        self.connection.commit()
        
    def get(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM comments WHERE id = ?", (str(id),))
        row = cursor.fetchone()
        return row
    
    def get_all(self, news_id = None):
        cursor = self.connection.cursor()
        if news_id:
            cursor.execute("SELECT * FROM comments WHERE news_id = ?",
                           (str(news_id),))
        else:
            cursor.execute("SELECT * FROM comments")
        rows = cursor.fetchall()
        return rows
    
    def news_delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM comments WHERE news_id = ?''', (str(news_id),))
        cursor.close()
        self.connection.commit()     
    
    def delete(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM comments WHERE id = ?''', (str(id),))
        cursor.close()
        self.connection.commit()    
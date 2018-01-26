# -*- coding: UTF-8 -*-

import sqlite3
from flask import g as flask_global
import os.path


class DBAccess(object):
    ''' Class which provides DB access ops. Connect, query, etc. Creates DB if not already exists.'''

    def __init__(self, app = None, schema = '', database = ''):
        self.app = app
        self.schema = schema
        self.database = database
        if not os.path.exists(database):
            self.init_db()
    
    def init_db(self):
        ''' Creates the sqlite DB from provided schema. '''
        
        with self.app.app_context():
            db = self.get_db()
            with self.app.open_resource(self.schema, mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
    
    def dict_factory(self, cursor, row):
        ''' Used to return query result rows as dictionaries '''
        
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))
        
    def get_db(self):
        ''' Returns a connection to this instance's database '''
        
        db = getattr(flask_global, '_database', None)
        if db is None:
            db = flask_global._database = sqlite3.connect(self.database)
        db.row_factory = self.dict_factory
        return db 
    
    def query_db(self, query, args=(), single=False):
        ''' Runs provided query with given parameters, optionally returning 1 row or all rows. '''
        
        curs = self.get_db().execute(query, args)
        results = curs.fetchall()
        curs.close()
        return (results[0] if results else None) if single else results
    
    def get_tasks(self):
        ''' Get the list of tasks on the list '''
        
        return self.query_db('''
        SELECT t.taskid,
          t.title,
          t.description,
          au.authorid,
          au.name AS author,
          au.email
        FROM task t,
          author au,
          task_author aa
        WHERE t.taskid = aa.taskid
        AND aa.authorid = au.authorid
        ORDER BY t.title ASC''')
    
    def add_task(self, _map):
        ''' Adds a new task to the list'''
        
        with self.get_db() as conn:
            try:
                conn.isolation_level = None
                curs = conn.cursor()                
                
                curs.execute("BEGIN TRANSACTION")
                curs.execute("insert into task (title, description) values (?, ?)",
                             (_map['title'], _map['description']))
                
                curs.execute("insert into author (name, email) values (?, ?)",
                             (_map['author'], _map['email']))
                
                curs.execute("""insert into task_author (taskid, authorid) values (
                    (SELECT last_insert_rowid() FROM task),
                    (SELECT last_insert_rowid() FROM author) )""")
                
                curs.execute("COMMIT")
            
            except conn.Error:
                print 'Caught error, rolling back'
                curs.execute("ROLLBACK")
    
    def update_task(self, _map):
        ''' Modifies an existing task's details '''
        
        with self.get_db() as conn:
            try:
                conn.isolation_level = None
                curs = conn.cursor()                
                
                curs.execute("BEGIN TRANSACTION")
                curs.execute("update task set title=?, description=? where taskid=?",
                             (_map['title'], _map['description'], _map['taskid']))
                
                curs.execute("update author set name=?, email=? where authorid=?",
                             (_map['author'], _map['email'], _map['authorid']))
                
                curs.execute("COMMIT")
            
            except conn.Error:
                print 'Caught error, rolling back'
                curs.execute("ROLLBACK")
        
        
#EOF        
# -*- coding: UTF-8 -*-

import sqlite3
from flask import g as flask_global
import os.path


class DBAccess(object):


    def __init__(self, app = None, schema = '', database = ''):
        self.app = app
        self.schema = schema
        self.database = database
        if not os.path.exists(database):
            self.init_db()
    
    def init_db(self):
        with self.app.app_context():
            db = self.get_db()
            with self.app.open_resource(self.schema, mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
    
    def dict_factory(self, cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))
        
    def get_db(self):
        db = getattr(flask_global, '_database', None)
        if db is None:
            db = flask_global._database = sqlite3.connect(self.database)
        db.row_factory = self.dict_factory
        return db 
    
    def query_db(self, query, args=(), single=False):
        curs = self.get_db().execute(query, args)
        results = curs.fetchall()
        curs.close()
        return (results[0] if results else None) if single else results
    
    def get_catalog(self):
        return self.query_db('''
        SELECT ap.appid,
          ap.title,
          ap.version,
          au.authorid,
          au.name AS author,
          au.email,
          au.company
        FROM app ap,
          author au,
          app_author aa
        WHERE ap.appid = aa.appid
        AND aa.authorid = au.authorid
        ORDER BY ap.title ASC''')
    
    def add_app(self, _map):
        
        with self.get_db() as conn:
            try:
                conn.isolation_level = None
                curs = conn.cursor()                
                
                curs.execute("BEGIN TRANSACTION")
                curs.execute("insert into app (title, version) values (?, ?)",
                             (_map['title'], _map['version']))
                
                curs.execute("insert into author (name, email, company) values (?, ?, ?)",
                             (_map['author'], _map['email'], _map['company']))
                
                curs.execute("""insert into app_author (appid, authorid) values (
                    (SELECT last_insert_rowid() FROM app),
                    (SELECT last_insert_rowid() FROM author) )""")
                
                curs.execute("COMMIT")
            
            except conn.Error:
                print 'Caught error, rolling back'
                curs.execute("ROLLBACK")
    
    def update_app(self, _map):
        with self.get_db() as conn:
            try:
                conn.isolation_level = None
                curs = conn.cursor()                
                
                curs.execute("BEGIN TRANSACTION")
                curs.execute("update app set title=?, version=? where appid=?",
                             (_map['title'], _map['version'], _map['appid']))
                
                curs.execute("update author set name=?, email=?, company=? where authorid=?",
                             (_map['author'], _map['email'], _map['company'], _map['authorid']))
                
                curs.execute("COMMIT")
            
            except conn.Error:
                print 'Caught error, rolling back'
                curs.execute("ROLLBACK")
        
        
#EOF        
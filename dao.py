# -*- coding: UTF-8 -*-

import sqlite3
from flask import Flask, g
app = Flask(__name__)

DATABASE = 'demo.sqlite'

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db

def query_db(query, args=(), single=False):
    curs = get_db().execute(query, args)
    results = curs.fetchall()
    curs.close()
    return (results[0] if results else None) if single else results

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('demo.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def getAllApps():
    
    sql = '''SELECT ap.title,
      ap.version,
      au.email,
      au.company
    FROM app ap,
      author au,
      app_author aa
    WHERE ap.appid = aa.appid
    AND aa.authorid = au.authorid
    ORDER BY ap.title ASC'''
    
    return query_db(sql)


# -*- coding: UTF-8 -*-
# run pip install flask

from flask import Flask, render_template, request, redirect, abort
import dao
import os

app = Flask(__name__)

db = dao.DBAccess(app = app, schema='demo.sql', database='demo.sqlite')
    
@app.route('/demo')
def home():
    return render_template('index.html', apps = db.get_catalog())


@app.route('/demo/create', methods=['POST'])
def add_new():

    if request.form['title'].strip() in ('', None):
        abort(400)
    else:
        params = {}
        for key in ('title','company','version','email','author'):
            params[key] = request.form[key]
        db.add_app(params)    
    
        return redirect('/demo', code=302)

@app.route('/demo/edit', methods=['POST'])
def edit_app():
    
    appid = request.form['appid']
    
    if request.form['title-' + appid].strip() in ('', None):
        abort(400)
    else:
        
        params = {}
        for key in map(lambda s: s + '-' + appid, ['title','company','version','email','author']) + ['appid','authorid']:
            params[key.rstrip('-' + appid)] = request.form[key]
        
        db.update_app(params)
    
        return redirect('/demo', code=302)

if __name__ == '__main__':
    app.run()
    ''' Now visit http://127.0.0.1:5000/demo '''
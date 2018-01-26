# -*- coding: UTF-8 -*-
# run pip install flask

from flask import Flask, render_template, request, redirect, abort
import dao

app = Flask(__name__)

db = dao.DBAccess(app = app, schema='demo.sql', database='demo.sqlite')
    
@app.route('/to-do')
def home():
    ''' Display the home page, the app catalog '''
    
    return render_template('index.html', tasks = db.get_tasks())


@app.route('/to-do/create', methods=['POST'])
def add_new():
    ''' Process POST from Add Task form '''
    
    if request.form['title'].strip() in ('', None):
        abort(400)
    else:
        params = {}
        for key in ('title','description','email','author'):
            params[key] = request.form[key]
        db.add_task(params)    
    
        return redirect('/to-do', code=302)

@app.route('/to-do/edit', methods=['POST'])
def edit_task():
    ''' Process POST from Edit Task form '''
    
    taskid = request.form['taskid']
    
    if request.form['title-' + taskid].strip() in ('', None):
        abort(400)
    else:
        params = {}
        for key in map(lambda s: s + '-' + taskid, ['title','description','email','author']) + ['taskid','authorid']:
            params[key.rstrip('-' + taskid)] = request.form[key]
        db.update_task(params)
    
        return redirect('/to-do', code=302)

if __name__ == '__main__':
    app.run()
    ''' Now visit http://127.0.0.1:5000/to-do '''
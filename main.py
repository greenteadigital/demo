# -*- coding: UTF-8 -*-
# pip install flask

from flask import Flask, render_template
import dao
import os
app = Flask(__name__)

if not os.path.exists(dao.DATABASE):
    dao.init_db()

@app.route('/demo')
def home():
        
    return render_template('index.html', apps = dao.getAllApps())

if __name__ == '__main__':
    app.run()

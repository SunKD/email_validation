from flask import Flask, render_template, request, redirect, flash
from mysqlconnection import MySQLConnector
from datetime import datetime
import re

app = Flask(__name__)
mysql = MySQLConnector(app, 'email')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app.secret_key = "this is Secret!!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    result = mysql.query_db(
        "SELECT email from emails where email = '{}'".format(request.form['email']))
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Email is not valid!", "error")
        return redirect('/')
    elif len(result) > 0:
        flash("Email already registered!", "error")
        return redirect('/')
    else:
        query = "INSERT INTO emails (email, created_at) values (:email, :date)"
        data ={
            'email': request.form['email'],
            'date': datetime.now()
        }
        flash("The email address you entered {} is a VALID email address. Thank You!!!".format(request.form['email']), "success")
        mysql.query_db(query, data)

        emails = mysql.query_db("SELECT * FROM emails")
        print emails
        return render_template('/success.html', emails = emails)

app.run(debug=True)
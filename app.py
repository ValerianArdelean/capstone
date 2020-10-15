from flask import Flask,render_template, jsonify,request,abort,redirect,url_for
from flask_cors import CORS
import json

from models import setup_db, Providers, Events, Customers, db
app = Flask(__name__)
setup_db(app)


@app.route('/')
def index():
    return('maa')

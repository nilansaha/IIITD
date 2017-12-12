from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd
import os
from plotly.offline import plot
from plotly.graph_objs import Bar, Pie
from query import *


app = Flask(__name__)

@app.route("/")
def index():
    return """There is nothing in this page. To view analysis on Delhi Air Pollution visit <a href="/delhi">here</a> and to view analysis on Mumbai Rains visit <a href="/mumbai">here</a>"""

@app.route("/delhi")
def delhi():
    divs = datainit('delhi')
    return render_template('index.html',hashtags=divs[0], retweets=divs[1], users=divs[2], sentiment=divs[3])


@app.route("/mumbai")
def mumbai():
    divs = datainit('mumbai')
    return render_template('index.html',hashtags=divs[0], retweets=divs[1], users=divs[2], sentiment=divs[3])

if __name__ == '__main__':
    port = int(os.environ.get('PORT',8080))
    app.run(host='0.0.0.0', port=port, threaded = True)

import pandas as pd
from flask import Flask, request, render_template, session, redirect
from flask import Flask
from OpenSSL import SSL
import datetime
from AllCode import *
now = datetime.datetime.now()

df = pd.read_csv('https://raw.githubusercontent.com/bartwitting/DSCS/master/afspeellijsten/Road.csv')
df = df[['title','artist']]
df.set_index(['title'], inplace=True)

app = Flask(__name__)

@app.route('/')
def dfpage():
    return render_template('home.html',tables=[df.to_html(classes='playlist')],

    titles = ['na', 'Current playlist'])

@app.route("/forward/", methods=['POST'])
def move_forward():
    #Moving forward code
    forward_message = Parameter_ranges(50, 10, 20, 100, 100, 15)
    return render_template('home.html', forward_message=forward_message);





if __name__ == '__main__':
    app.run(debug=True)

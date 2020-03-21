import pandas as pd
from flask import Flask, request, render_template, session, redirect, url_for

from OpenSSL import SSL
from datetime import datetime as time_
from datetime import date
import time
from AllCode import *
import itertools

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods = ['GET','POST'])
def dfpage():
    return render_template('index.html')


@app.route("/forward/", methods=['GET','POST'])
def move_forward():
    if request.method == 'POST':
        print ('hallo!!!')
        Spotusername = request.form['Username']
        Playlink = request.form['Spotifylink']
        weatherPlace = request.form['placeWeather']
        session['Username'] = Spotusername
        session ['placeWeather'] = weatherPlace 
        #df = pd.read_csv('https://raw.githubusercontent.com/bartwitting/DSCS/master/afspeellijsten/Road.csv')
        #df = df[['title','artist']]
        SaveIDs(Spotusername,Playlink, weatherPlace)
        results = Start(True)
        df = results[1]
        forward_message = results[0]
        features = forward_message[0]
        sources=forward_message[1]
        sources1 = [item for t in sources for item in t]
        features1= [item for t in features for item in t]
        print(sources1)
        return render_template('playlists.html',features=features1, sources=sources1,tables =[df.to_html(classes='playlist')],titles = ['na', 'Current playlist'], Username=Spotusername, Weatherplace=weatherPlace)

    else:
        results = Start(False)
        df = results[1]
        forward_message = results[0]
        features = forward_message[0]
        sources=forward_message[1]
        sources1 = [item for t in sources for item in t]
        features1= [item for t in features for item in t]
        return render_template('playlists.html',features=features1, sources=sources1,tables =[df.to_html(classes='playlist')],titles = ['na', 'Current playlist'],Username=session['Username'] , Weatherplace=session['placeWeather'])

if __name__ == '__main__':
    app.run(debug=True)

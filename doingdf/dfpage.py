import pandas as pd
from flask import Flask, request, render_template, session, redirect, url_for

from OpenSSL import SSL
from datetime import datetime as time_
from datetime import date
import time
from AllCode import *


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
        #df = pd.read_csv('https://raw.githubusercontent.com/bartwitting/DSCS/master/afspeellijsten/Road.csv')
        #df = df[['title','artist']]
        SaveIDs(Spotusername,Playlink)
        results = Start(True)
        df = results[1]
        forward_message = results[0]
        return render_template('playlists.html',forward_message=forward_message,tables =[df.to_html(classes='playlist')],titles = ['na', 'Current playlist'], Username=Spotusername, Spotifylink=Playlink)

    else:
        results = Start(False)
        df = results[1]
        forward_message = results[0]
        return render_template('playlists.html',forward_message=forward_message,tables =[df.to_html(classes='playlist')],titles = ['na', 'Current playlist'])

if __name__ == '__main__':
    app.run(debug=True)

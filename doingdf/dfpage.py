import pandas as pd
from flask import Flask, request, render_template, session, redirect, url_for

from OpenSSL import SSL
from datetime import datetime as time_
from datetime import date
import time
from AllCode import *
#now = datetime.datetime.now()

#df = pd.read_csv('https://raw.githubusercontent.com/bartwitting/DSCS/master/afspeellijsten/Road.csv')
#df = df[['title','artist']]
#df.set_index(['title'], inplace=True)
#text-shadow: 1px 0 0 #000, 0 -1px 0 #000, 0 1px 0 #000, -1px 0 0 #000;
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods = ['GET','POST'])
def dfpage():
    return render_template('index.html')




@app.route("/forward/", methods=['GET','POST'])
def move_forward():
    #Username = session['Username']
    #Spotifylink = session['Spotifylink']
    #iliketrains = request.form['iliketrains']
    if request.method == 'POST':
        print ('hallo!!!')
        Spotusername = request.form['Username']
        Playlink = request.form['Spotifylink']
        return render_template('playlists.html', forward_message=forward_message,tables =[df.to_html(classes='playlist')],titles = ['na', 'Current playlist'], Username=Spotusername, Spotifylink=Playlink)


    else:

        now = time_.now()
        forward_message = now
        df = pd.read_csv('https://raw.githubusercontent.com/bartwitting/DSCS/master/afspeellijsten/Road.csv')
        df = df[['title','artist']]

        time.sleep(10)
        #print(brew_type)
        return render_template('playlists.html', forward_message=forward_message,tables =[df.to_html(classes='playlist')],titles = ['na', 'Current playlist'], Username=Spotusername, Spotifylink=Playlink)




if __name__ == '__main__':
    app.run(debug=True)

import pandas as pd
from flask import Flask, request, render_template, session, redirect
from flask import Flask
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

@app.route('/', methods=['POST','GET'])
def dfpage():
    if request.method == 'POST':
        print ('hallo!!!')
        item = request.form['Username']
        print (item)
        session["Username"]=item
        session['Spotifylink']= request.form.get("Spotifylink", 'sukkel')
        return render_template('index.html')
    else:
        print('wtf is dit')
        return render_template('index.html')


      #return render_template('index.html')
      #return render_template('index.html',haha1=Username,haha2=Spotifylink)



@app.route("/forward/", methods=['POST','GET'])
def move_forward():
    #Username = session['Username']
    #Spotifylink = session['Spotifylink']
    #iliketrains = request.form['iliketrains']
    Username = session.get('Username')
    print (Username)
    Spotifylink=session.get('Spotifylink')
    now = time_.now()
    forward_message = now
    df = pd.read_csv('https://raw.githubusercontent.com/bartwitting/DSCS/master/afspeellijsten/Road.csv')
    df = df[['title','artist']]

    time.sleep(10)
        #print(brew_type)
    return render_template('playlists.html', forward_message=forward_message,tables =[df.to_html(classes='playlist')],titles = ['na', 'Current playlist'], Username=Username, Spotifylink=Spotifylink)

    #df.set_index(['title'], inplace=True)
    #, Spotifylink=session['Spotifylink'])


if __name__ == '__main__':
    app.run(debug=True)

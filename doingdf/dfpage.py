import pandas as pd
from flask import Flask, request, render_template, session, redirect

df = pd.read_csv('https://raw.githubusercontent.com/bartwitting/DSCS/master/afspeellijsten/Road.csv')
df = df[['title','artist']]
df.set_index(['title'], inplace=True)

from flask import Flask
from OpenSSL import SSL



app = Flask(__name__)

@app.route('/')
def dfpage():
    return render_template('home.html',tables=[df.to_html(classes='playlist')],

    titles = ['na', 'Current playlist'])

@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return ("nothing")






if __name__ == '__main__':
    app.run(debug=True)

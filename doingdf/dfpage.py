import pandas as pd
from flask import Flask, request, render_template, session, redirect

df = pd.read_csv('https://raw.githubusercontent.com/bartwitting/DSCS/master/afspeellijsten/Road.csv')
df = df[['title','artist']]
df.set_index(['title'], inplace=True)

from flask import Flask
from OpenSSL import SSL

context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
context.use_privatekey_file('server.key')
context.use_certificate_file('server.crt')

app = Flask(__name__)

@app.route('/')
def dfpage():
    return render_template('home.html',tables=[df.to_html(classes='playlist')],

    titles = ['na', 'Current playlist'])


@app.route('/', methods=['POST', 'GET'])
def button():
    if request.method == "POST":
        print ('Hello world!')

    return render_template('home.html')




if __name__ == '__main__':
    app.run(debug=True)

import pandas as pd
from flask import Flask, request, render_template, session, redirect

df = pd.read_csv('https://raw.githubusercontent.com/bartwitting/DSCS/master/afspeellijsten/Road.csv')


from flask import Flask

app = Flask(__name__)

@app.route('/')
def dfpage():
    return df.to_html(header="true")

if __name__ == '__main__':
    app.run(debug=True)

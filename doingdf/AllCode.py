import os
import json
import random
from pyowm import OWM
from pyowm.caches.lrucache import LRUCache
import datetime
import math
import subprocess
from statistics import mean

import sys
import spotipy
import spotipy.util as util
import pandas as pd
import numpy as np
sp = spotipy.Spotify()

API_key = '6ff7fde73bb9cccf854fd26d31b4fe6d'
owm = OWM(API_key)
cache = LRUCache()


########################################################################################################################################

userURL = ""
userIDSpotify = ""
playlistID = ""

def get_playlist_tracks(credentials,username,playlist_id):
    #set scope to retreive public data
    scope_playlist = 'playlist-modify-public'
    #provide token using given credentials
    #credentials are: username, public key, private key and redirect_uri
    token = util.prompt_for_user_token(credentials[0],scope_playlist,credentials[1],credentials[2],credentials[3])
    sp = spotipy.Spotify(auth=token)
    #get tracklisting from playlist data
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    #ensure collection of data after more than 100 requests
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def get_features(tracks):
    #set scope to retreive public data
    scope_playlist = 'playlist-modify-public'
    #provide token using given credentials
    #credentials are: username, public key, private key and redirect_uri
    token = util.prompt_for_user_token(credentials[0],scope_playlist,credentials[1],credentials[2],credentials[3])
    sp = spotipy.Spotify(auth=token)
    #make empty list to collect dictionaries for dataframe
    dataframe = []
    for x in tracks:
        try:
            track = x['track']
            #get audio features per track
            feat = (sp.audio_features(tracks=[track['id']])[0])
            #get track and artist info
            art_dict = {'artist':track['artists'][0]['name'], 'title':track['name'], 'popularity':track['popularity']}
            #combine both dictionaries
            art_dict.update(feat)
            #make dataframe from dictionary
            dataframe.append(art_dict)
        except:
            print("Oh no!",sys.exc_info()[0],"happend")
    #filter dataframe to neccesary columns
    df = pd.DataFrame(dataframe)
    df = df.filter(['title', 'artist', 'danceability','energy', 'loudness', 'tempo','valence', 'popularity','id'])
    df = df.set_index('title')
    return df

def add_tracks_from_df(credentials,playlist,dataframe,features):
    scope_playlist = 'playlist-modify-public'
    token = util.prompt_for_user_token(credentials[0],scope_playlist,credentials[1],credentials[2],credentials[3])
    sp = spotipy.Spotify(auth=token)
    #make selection based on feature input
    selection = dataframe.loc[(dataframe['danceability'].between(features[0]-0.1, features[0]+0.1, inclusive=False)) &\
    (dataframe['energy'].between(features[1]-0.2, features[1]+0.2, inclusive=False)) &\
    (dataframe['loudness'].between(features[2]-5, features[2]+5, inclusive=False)) &\
    (dataframe['tempo'].between(features[3]-40, features[3]+40, inclusive=False)) &\
    (dataframe['valence'].between(features[4]-0.5, features[4]+0.5, inclusive=False)) &\
    #remove unwanted artists
    (~dataframe['artist'].isin(['Ariana Grande']))]
    selection.sort_values(by=['popularity'], ascending=False)
    songs = selection['id'].tolist()
    
    scope_playlist = 'playlist-modify-public'
    token2 = util.prompt_for_user_token(credentials[0],scope_playlist,credentials[1],credentials[2],credentials[3])
    sp2 = spotipy.Spotify(auth=token2)
    sp2.user_playlist_add_tracks(credentials[0],playlist, songs)
    print("Songs Succesfully Added to Playlist")
    
def remove_tracks_from_df(credentials,playlist,dataframe,features):
    scope_playlist = 'playlist-modify-public'
    token = util.prompt_for_user_token(credentials[0],scope_playlist,credentials[1],credentials[2],credentials[3])
    sp = spotipy.Spotify(auth=token)
    selection = dataframe.loc[(dataframe['danceability'].between(features[0]-0.1, features[0]+0.1, inclusive=False)) &\
    (dataframe['energy'].between(features[1]-0.2, features[1]+0.2, inclusive=False)) &\
    (dataframe['loudness'].between(features[2]-5, features[2]+5, inclusive=False)) &\
    (dataframe['tempo'].between(features[3]-40, features[3]+40, inclusive=False)) &\
    (dataframe['valence'].between(features[4]-0.5, features[4]+0.5, inclusive=False))]
    selection.sort_values(by=['popularity'], ascending=False)
    songs = selection['id'].tolist()
    
    scope_playlist = 'playlist-modify-public'
    token2 = util.prompt_for_user_token(credentials[0],scope_playlist,credentials[1],credentials[2],credentials[3])
    sp2 = spotipy.Spotify(auth=token2)
    sp2.user_playlist_remove_all_occurrences_of_tracks(credentials[0],playlist, songs)
    print("Songs Succesfully Removed from Playlist")

credentials = ['bartw26396', '5711bc132b4c48ceb5bbd19cd65b1e63', 'f507991961c948d8bf1b62ae6ef5ab15', 'http://localhost']
tracklist = get_playlist_tracks(credentials, 'tillyxh','1TFZPafSKEeh31U9fky1vW')

musicData = get_features(tracklist)


########################################################################################################################################

#ranges

decibel_low= range(0,50)
decibel_medium= range(50,70)
decibel_noise= range(70,90)
decibel_loud= range(90,151)

decibel_list= [("decibel_low",decibel_low), ("decibel_medium",decibel_medium), ("decibel_noise",decibel_noise), ("decibel_loud",decibel_loud)]

people_little= range(0,10)
people_medium= range(10,20)
people_busy= range(20,30)
people_crowded= range(30,101)

people_list= [('people_little',people_little), ('people_medium',people_medium), ('people_busy',people_busy), ('people_crowded',people_crowded)]

temperature_freezing= range(-10, 5)
temperature_cold= range(5,15)
temperature_warm= range(15,25)
temperature_hot= range(25,45)

temperature_list = [('temperature_freezing',temperature_freezing), ('temperature_cold',temperature_cold) , ('temperature_warm',temperature_warm), ('temperature_hot',temperature_hot)]

rain_little= range(0,20)
rain_some= range(20,40)
rain_medium= range(40,60)
rain_much= range(60,80)
rain_heavy = range(80,101)

rain_list= [('rain_little',rain_little ), ('rain_some',rain_some), ('rain_medium',rain_medium), ('rain_much',rain_much), ('rain_heavy',rain_heavy)]

clouds_little= range(0,20)
clouds_some= range(20,40)
clouds_medium= range(40,60)
clouds_much= range(60,80)
clouds_only= range(80,101)

clouds_list= [('clouds_little',clouds_little), ('clouds_some',clouds_some), ('clouds_medium',clouds_medium), ('clouds_much',clouds_much), ('clouds_only',clouds_only)]

time_early= range(9,11)
time_beforelunch= range(11,13)
time_afterlunch= range(13,17)
time_closing= range(17,18)

time_list= [('time_early',time_early), ('time_beforelunch',time_beforelunch), ('time_afterlunch',time_afterlunch), ('time_closing',time_closing)]



########################################################################################################################################




def filebuild():
    if os.path.exists("mac_adresses.json"):
        os.remove("mac_adresses.json")
    else: 
        os.system("howmanypeoplearearound --out mac_adresses.json --adapter en0 --scantime 20 --sort")
        
def WifiNum() :
	filebuild()
	with open('mac_adresses.json') as file:
		data = json.load(file)

	all_cellphones = [x for x in data['cellphones']]
	threshold = -67
	cellphones_within_threshold = [x for x in all_cellphones if x['rssi'] > threshold]
	filebuild()
	print("WifiNum OK")
	return len(cellphones_within_threshold)

def DecibelNum():
    batcmd="soundmeter --collect --seconds 5" 
    result1 = subprocess.check_output(batcmd, shell=True) 
    average_rms = int(result1[-7:-1])
    amount_of_db = 20 * math.log10(average_rms)
    amount_of_db_rounded = round(amount_of_db, 2)
    print("DecibelNum OK")
    return amount_of_db_rounded

def WeatherNum() :
    place = owm.weather_at_place('Muiden,NL')
    weathercall = place.get_weather()
    cloudiness = weathercall.get_clouds()
    rain_status = weathercall.get_rain()
    if len(rain_status) > 0:
        rkeys = list(rain_status.keys())
        rain_mm = rain_status[rkeys[0]]
    else:
        rain_mm = 0
    temperature = weathercall.get_temperature(unit='celsius')['temp']
    print("WeatherNum OK")
    return [cloudiness,rain_mm, temperature]
    
def getNums() :
    numPeople = WifiNum()
    decibel = DecibelNum()
    weather = WeatherNum()
    temperature = weather[2]
    clouds = weather[0]
    rain = weather[1]
    now = datetime.datetime.now()
    time = now.hour
    print("GetNums OK")
    return decibel, numPeople, temperature, rain, clouds, time


########################################################################################################################################



def Parameter_ranges(decibel, people, temperature, rain, clouds, time):
    ruis_range= str
    mensen_range = str
    temp_range = str
    regen_range = str
    wolk_range = str
    uur_range = str
  
    for ruis in decibel_list:
        for db in ruis[1]:
            if db == decibel:
                ruis_range = ruis[0]
            
    for mensen in people_list:
        for mens in mensen[1]:
            if mens==people:
                mensen_range = mensen[0]
            
    for temp in temperature_list:
        for c in temp[1]:
            if c==temperature:
                temp_range = temp[0]
    
    for regen in rain_list:
        for m in regen[1]:
            if m==rain:
                regen_range = regen[0]
            
    for wolk in clouds_list:
        for w in wolk[1]:
            if w==clouds:
                wolk_range = wolk[0]
    
    for uur in time_list:
        for s in uur[1]:
            if s==time:
                uur_range = uur[0]
    
    return ruis_range, mensen_range, temp_range, regen_range, wolk_range, uur_range


def Danceability(decibel, people, temperature, rain, clouds, time):
    
    parameter_returns= Parameter_ranges(decibel, people, temperature, rain, clouds, time)
    
    score_ruis= 0
    score_mens= 0
    score_temp= 0
    score_regen= 0
    score_wolk= 0 
    score_uur = 0
    score_total = 0
    
    decibel_tuple= [("decibel_low", 9), ("decibel_medium",7), ("decibel_noise",6),("decibel_loud",3)]
    people_tuple= [('people_little',9), ('people_medium',7), ('people_busy',5), ('people_crowded',4)]
    temperature_tuple = [('temperature_freezing',4), ('temperature_cold',6) , ('temperature_warm',8), ('temperature_hot',9)]
    rain_tuple = [('rain_little',9), ('rain_some',7), ('rain_medium',6), ('rain_much',4), ('rain_heavy',3)]
    clouds_tuple = [('clouds_little',9), ('clouds_some',7), ('clouds_medium',6), ('clouds_much',5), ('clouds_only',4)]
    time_tuple = [('time_early',5), ('time_beforelunch',7), ('time_afterlunch',9), ('time_closing',5)]
    
    for x in decibel_tuple:
        if x[0] == parameter_returns[0]:
            score_ruis = x[1]*30
    
    for x in people_tuple:
        if x[0] == parameter_returns[1]:
            score_mens = x[1]*20
            
    for x in temperature_tuple:
        if x[0] == parameter_returns[2]:
            score_temp = x[1]*15
    
    for x in rain_tuple:
        if x[0] == parameter_returns[3]:
            score_regen = x[1]*5
    
    for x in clouds_tuple:
        if x[0] == parameter_returns[4]:
            score_wolk = x[1]*10
    
    for x in time_tuple:
        if x[0] == parameter_returns[5]:
            score_uur = x[1]*20
    
    da_total= (score_ruis + score_mens + score_temp + score_regen + score_wolk + score_uur)/1000
    return da_total

def Energy(decibel, people, temperature, rain, clouds, time):
    
    parameter_returns= Parameter_ranges(decibel, people, temperature, rain, clouds, time)
    
    score_ruis= 0
    score_mens= 0
    score_temp= 0
    score_regen= 0
    score_wolk= 0 
    score_uur = 0
    score_total = 0
    
    decibel_tuple= [("decibel_low", 9), ("decibel_medium",7), ("decibel_noise",4),("decibel_loud",2)]
    people_tuple= [('people_little',8), ('people_medium',7), ('people_busy',6), ('people_crowded',4)]
    temperature_tuple = [('temperature_freezing',5), ('temperature_cold',7) , ('temperature_warm',8), ('temperature_hot',9)]
    rain_tuple = [('rain_little',9), ('rain_some',7), ('rain_medium',5), ('rain_much',4), ('rain_heavy',2)]
    clouds_tuple = [('clouds_little',9), ('clouds_some',8), ('clouds_medium',6), ('clouds_much',5), ('clouds_only',4)]
    time_tuple = [('time_early',4), ('time_beforelunch',6), ('time_afterlunch',9), ('time_closing',3)]
    
    for x in decibel_tuple:
        if x[0] == parameter_returns[0]:
            score_ruis = x[1]*30
    
    for x in people_tuple:
        if x[0] == parameter_returns[1]:
            score_mens = x[1]*20
            
    for x in temperature_tuple:
        if x[0] == parameter_returns[2]:
            score_temp = x[1]*15
    
    for x in rain_tuple:
        if x[0] == parameter_returns[3]:
            score_regen = x[1]*5
    
    for x in clouds_tuple:
        if x[0] == parameter_returns[4]:
            score_wolk = x[1]*10
    
    for x in time_tuple:
        if x[0] == parameter_returns[5]:
            score_uur = x[1]*20
    
    en_total= (score_ruis + score_mens + score_temp + score_regen + score_wolk + score_uur)/1000
    return en_total

def Loudness(decibel, people, temperature, rain, clouds, time):
    parameter_returns= Parameter_ranges(decibel, people, temperature, rain, clouds, time)
    
    score_ruis= 0
    score_mens= 0
    score_uur = 0
    score_total = 0
    
    decibel_tuple= [("decibel_low", 9), ("decibel_medium",6), ("decibel_noise",3),("decibel_loud",1)]
    people_tuple= [('people_little',9), ('people_medium',6), ('people_busy',4), ('people_crowded',2)]
    time_tuple = [('time_early',4), ('time_beforelunch',7), ('time_afterlunch',8), ('time_closing',4)]
    
    for x in decibel_tuple:
        if x[0] == parameter_returns[0]:
            score_ruis = x[1]*50
    
    for x in people_tuple:
        if x[0] == parameter_returns[1]:
            score_mens = x[1]*20
    
    for x in time_tuple:
        if x[0] == parameter_returns[5]:
            score_uur = x[1]*30
    
    lo_total= (score_ruis + score_mens + score_uur)/10
    value = ((lo_total * (0 - -30) / 100) + -30)
    return value

def Tempo(decibel, people, temperature, rain, clouds, time):
    parameter_returns= Parameter_ranges(decibel, people, temperature, rain, clouds, time)
    
    score_ruis= 0
    score_mens= 0
    score_temp= 0
    score_uur = 0
    score_total = 0
    
    decibel_tuple= [("decibel_low", 9), ("decibel_medium",7), ("decibel_noise",5),("decibel_loud",3)]
    people_tuple= [('people_little',8), ('people_medium',7), ('people_busy',4), ('people_crowded',3)]
    temperature_tuple = [('temperature_freezing',5), ('temperature_cold',7) , ('temperature_warm',9), ('temperature_hot',5)]
    time_tuple = [('time_early',4), ('time_beforelunch',9), ('time_afterlunch',6), ('time_closing',4)]
    
    for x in decibel_tuple:
        if x[0] == parameter_returns[0]:
            score_ruis = x[1]*30
    
    for x in people_tuple:
        if x[0] == parameter_returns[1]:
            score_mens = x[1]*20
                               
    for x in temperature_tuple:
        if x[0] == parameter_returns[2]:
            score_temp = x[1]*20
    
    for x in time_tuple:
        if x[0] == parameter_returns[5]:
            score_uur = x[1]*30
    
    lo_total= (score_ruis + score_mens + score_temp+ score_uur)/10
    value = ((lo_total * (200 - 50) / 100) + 50)
    return value

def Valence(decibel, people, temperature, rain, clouds, time):
    parameter_returns= Parameter_ranges(decibel, people, temperature, rain, clouds, time)
    
    score_ruis= 0
    score_mens= 0
    score_temp= 0
    score_regen= 0
    score_wolk= 0 
    score_uur = 0
    score_total = 0
    
    decibel_tuple= [("decibel_low", 9), ("decibel_medium",7), ("decibel_noise",5),("decibel_loud",3)]
    people_tuple= [('people_little',9), ('people_medium',7), ('people_busy',5), ('people_crowded',4)]
    temperature_tuple = [('temperature_freezing',3), ('temperature_cold',5) , ('temperature_warm',10), ('temperature_hot',8)]
    rain_tuple = [('rain_little',8), ('rain_some',7), ('rain_medium',5), ('rain_much',4), ('rain_heavy',3)]
    clouds_tuple = [('clouds_little',10), ('clouds_some',8), ('clouds_medium',6), ('clouds_much',4), ('clouds_only',3)]
    time_tuple = [('time_early',4), ('time_beforelunch',9), ('time_afterlunch',7), ('time_closing',5)]
    
    for x in decibel_tuple:
        if x[0] == parameter_returns[0]:
            score_ruis = x[1]*30
    
    for x in people_tuple:
        if x[0] == parameter_returns[1]:
            score_mens = x[1]*20
            
    for x in temperature_tuple:
        if x[0] == parameter_returns[2]:
            score_temp = x[1]*15
    
    for x in rain_tuple:
        if x[0] == parameter_returns[3]:
            score_regen = x[1]*5
    
    for x in clouds_tuple:
        if x[0] == parameter_returns[4]:
            score_wolk = x[1]*10
    
    for x in time_tuple:
        if x[0] == parameter_returns[5]:
            score_uur = x[1]*20
    
    va_total= (score_ruis + score_mens + score_temp + score_regen + score_wolk + score_uur)/1000
    return va_total

def RunAll(bron):
    decibel, people, temperature, rain, clouds, time = bron[0], bron[1], bron[2], bron[3], bron[4], bron[5]
    danceability = Danceability(decibel, people, temperature, rain, clouds, time)
    energy = Energy(decibel, people, temperature, rain, clouds, time)
    loudness= Loudness(decibel, people, temperature, rain, clouds, time)
    tempo= Tempo(decibel, people, temperature, rain, clouds, time)
    valence= Valence(decibel, people, temperature, rain, clouds, time)
    print("RunAll OK")
    return [danceability, energy, loudness, tempo, valence]




def spotifyListBuilder(ocredentials,musicData):
    surroundings = getNums()
    features = RunAll(surroundings)
    add_tracks_from_df(credentials,'5yJfsUa3aWq20QhPLGwtig',musicData,features)
    
    return features,surroundings

spotifyListBuilder(credentials,musicData)

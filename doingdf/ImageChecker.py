from IPython.display import Image 
from PIL import Image
import requests
from io import BytesIO
print(sp.current_user_playing_track()['item']['artists'][0]['name'])
print(sp.current_user_playing_track()['item']['name'])
response = requests.get(sp.current_user_playing_track()['item']['album']['images'][0]['url'])
img = Image.open(BytesIO(response.content))
img

def check_song():
    current_song = sp.current_user_playing_track()['item']['name']
    current_artist = sp.current_user_playing_track()['item']['artists'][0]['name']
    current_song = sp.current_user_playing_track()['item']['name']
    response = requests.get(sp.current_user_playing_track()['item']['album']['images'][0]['url'])
    current_img = Image.open(BytesIO(response.content))
    print(current_artist)
    print(current_song)
    display(current_img)
    while current_song == sp.current_user_playing_track()['item']['name']:
        current_artist = sp.current_user_playing_track()['item']['artists'][0]['name']
        current_song = sp.current_user_playing_track()['item']['name']
        response = requests.get(sp.current_user_playing_track()['item']['album']['images'][0]['url'])
        current_img = Image.open(BytesIO(response.content))
    else:
        current_artist = sp.current_user_playing_track()['item']['artists'][0]['name']
        current_song = sp.current_user_playing_track()['item']['name']
        response = requests.get(sp.current_user_playing_track()['item']['album']['images'][0]['url'])
        current_img = Image.open(BytesIO(response.content))
        print(current_artist)
        print(current_song)
        display(current_img)
        check_song()
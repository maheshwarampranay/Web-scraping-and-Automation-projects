from bs4 import BeautifulSoup
import requests
import re, spotipy
from spotipy.oauth2 import SpotifyOAuth
client_id = '3aa0f9cbfd1f45b59fa4d283b8f3eef4'
client_secret = '62a3d2829bb94bfbb35c867aacec6db9'


def get_top_100(date):
    url = f"https://www.billboard.com/charts/hot-100/{date}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    songs = [i.text for i in soup.select('li h3')]
    songs = [re.search('\w.*\w',i).group() for i in songs]
    return songs[:100]

date = input('enter date in YYYY-MM-DD format:\n')
year = date.split('-')[0]
songs_list = get_top_100(date)
#print(songs_list)
#print(songs_list[-1])

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username='Pranay Maheshwaram',
    )
)
user_id = sp.current_user()["id"]
#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    #print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Musical Journey", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
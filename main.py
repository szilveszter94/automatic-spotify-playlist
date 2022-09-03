import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# get the year from the user
years = input("Type the year in YYY-MM-DD format: ")

# insert the year into the url
response = requests.get(f"https://www.billboard.com/charts/hot-100/{years}")
billboard_page = response.text
soup = BeautifulSoup(billboard_page, "html.parser")
# find all music titles with BeautifulSoup
music_title = soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 "
                                              "lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 "
                                              "u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 "
                                              "u-max-width-230@tablet-only")
# find all artists titles with BeautifulSoup
artist = soup.find_all(name="span", class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max "
                                           "u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block "
                                           "a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")
# format all song names
unformatted_songs = []
formatted_songs = []
for i in music_title:
    unformatted_songs.append(i.getText())
for i in unformatted_songs:
    z = i.split("\n")
    formatted_songs.append(z[1])

# format all artists names (not used)
# unformatted_artists = []
# formatted_artists = []
# for i in artist:
#     unformatted_artists.append(i.getText())
# for i in unformatted_artists:
#     z = i.split("\n")
#     formatted_artists.append(z[1])

# spotify authentication with individual key
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="CLIENT_ID",
                                               client_secret="CLIENT_SECRET",
                                               redirect_uri="http://127.0.0.1:5500/", state=None,
                                               scope="playlist-modify-private", cache_path="YOUR CACHE PATH", username=None,
                                               proxies=None, show_dialog=True, requests_session=True,
                                               requests_timeout=None))
# get the user ID
user_id = sp.current_user()["id"]
date = years
song_names = formatted_songs

# create array for spotify song uris
song_uris = []
year = years.split("-")[0]
# search all song names on spotify
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
# create an empty playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# add all songs to playlist from the song uris array
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
#best version

#creates NEW playlist from walking songs in many playlists

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import spotipy.util as util
import pandas as pd
import numpy as np
import math
import constants


client_id = constants.my_client_id
client_secret = constants.my_client_secret
username=constants.my_username

token = util.prompt_for_user_token(username=username, scope='playlist-modify-private,playlist-modify-public', client_id=client_id, client_secret=client_secret, 
	redirect_uri='http://localhost:8080')

sp = spotipy.Spotify(auth=token)


def walk_from_many(playlist_name,playlist_list):

	ids=[]
	artists=[]
	songs=[]
	popularity=[]
	audio_features=[]


	sp.user_playlist_create(username, name=playlist_name)

	playlists = sp.user_playlists(username)
	for playlist in playlists['items']:  # iterate through playlists I follow
		if playlist['name'] == playlist_name:  # filter for newly created playlist
			playlist_id = playlist['id']

	for i in range(len(playlist_list)):
		results = sp.user_playlist_tracks(username,playlist_list[i])
		tracks = results['items']
		while results['next']:
			results = sp.next(results)
			tracks.extend(results['items'])
		for item in tracks:
			ids.append(item['track']['uri'])
			artists.append(item['track']['artists'][0]['name'])
			songs.append(item['track']['name'])
			popularity.append(item['track']['popularity'])
			audio_features.append(sp.audio_features(item['track']['uri']))

	bpm=([audio_features[i][0]['tempo'] for i in range(len(ids))])

	df= pd.DataFrame([ids, artists, songs, bpm, popularity], index=['ids','artists','songs','bpm','popularity']).T


	df=df.drop_duplicates()

	df = df[df['bpm']>=110]
	df = df[df['bpm']<=130]



	df=df.sort_values('bpm',ascending=True)


	df = np.array_split(df, math.ceil(len(df)/100))

	print(df)

	for i in df:
		sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=i['ids'])








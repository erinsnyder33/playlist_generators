#creates NEW playlist that is all the bpm of ONE song

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

def walk_one_song(search_string, playlist_list, closeness):

	ids=[]
	artists=[]
	songs=[]
	popularity=[]
	audio_features=[]


	results = sp.search(q=search_string, limit=1, type='track') #get 5 responses since first isn't always accurate
	search_song_uri=results['tracks']['items'][0]['uri']

	search_audio_features=(sp.audio_features(search_song_uri))

	search_bpm=(search_audio_features[0]['tempo'])

	print(search_bpm)
	#print(search_bpm)


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

	print(df)

	df = df[df['bpm']>search_bpm-closeness]
	df = df[df['bpm']<search_bpm+closeness]



	df=df.sort_values('bpm',ascending=True)


	df = np.array_split(df, math.ceil(len(df)/100))

	print(df)



	playlist_name = f"Music with bpm of {search_string}"    
	sp.user_playlist_create(username, name=playlist_name)

	playlists = sp.user_playlists(username)
	for playlist in playlists['items']:  # iterate through playlists I follow
		if playlist['name'] == playlist_name:  # filter for newly created playlist
			playlist_id = playlist['id']


	for i in df:
		sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=i['ids'])








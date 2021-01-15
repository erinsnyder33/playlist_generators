
#finds my preferences in music
#looks at most played tracks and shows pdf of different musical traits

import statistics
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import spotipy.util as util
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import seaborn as sns
import mpld3
import constants


client_id = constants.my_client_id
client_secret = constants.my_client_secret
username=constants.my_username

token = util.prompt_for_user_token(username=username, scope='playlist-modify-private,playlist-modify-public,user-library-read, user-top-read', client_id=client_id, client_secret=client_secret, 
	redirect_uri='http://localhost:8080')

sp = spotipy.Spotify(auth=token)


def make_pdf_plot(time_range):
	top_tracks=(sp.current_user_top_tracks(limit=50, offset=0, time_range=time_range))

	artists=[]
	songs=[]
	ids=[]

	for i in top_tracks['items']:
		artists.append(i['artists'][0]['name'])
		songs.append(i['name'])
		ids.append(i['id'])


	audio_features=(sp.audio_features(ids))


	acousticness=([audio_features[i]['acousticness'] for i in range(len(ids))])
	danceability=([audio_features[i]['danceability'] for i in range(len(ids))])
	duration_ms=([audio_features[i]['duration_ms'] for i in range(len(ids))])
	energy=([audio_features[i]['energy'] for i in range(len(ids))])
	instrumentalness=([audio_features[i]['instrumentalness'] for i in range(len(ids))])
	key=([audio_features[i]['key'] for i in range(len(ids))])
	liveness=([audio_features[i]['liveness'] for i in range(len(ids))])
	loudness=([audio_features[i]['loudness'] for i in range(len(ids))])
	mode=([audio_features[i]['mode'] for i in range(len(ids))])
	speechiness=([audio_features[i]['speechiness'] for i in range(len(ids))])
	tempo=([audio_features[i]['tempo'] for i in range(len(ids))])
	time_signature=([audio_features[i]['time_signature'] for i in range(len(ids))])
	valence=([audio_features[i]['valence'] for i in range(len(ids))])

	parameters=[acousticness,danceability,duration_ms,energy,instrumentalness,key,liveness,loudness,mode,speechiness,tempo,time_signature,valence]
	labels=['acousticness','danceability','duration_ms','energy','instrumentalness','key','liveness','loudness','mode','speechiness','tempo','time_signature','valence']


	avgs=[]
	Q1=[]
	Q3=[]
	for i in range(len(parameters)):
		Q1.append(np.percentile(parameters[i], 25, interpolation = 'midpoint'))
		avgs.append(statistics.mean(parameters[i]))
		Q3.append(np.percentile(parameters[i], 75, interpolation = 'midpoint'))



	short_description=[
	'1=Acoustic, 0=Not acoustic',
	'1=Most danceable, 0=Least danceable. Based on tempo, rhythm stability, beat strength, and overall regularity.',
	'Track length in milliseconds',
	'1=High energy, 0=Low energy. Based on if it is fast, loud, and noisy',
	'1=No vocal content, 0=Vocal Content',
	'0 = C, 1 = C♯/D♭, 2 = D, and so on. -1=No key detected.',
	'1=Performed Live, 0=Not Live',
	'-60(db)=Quieter, 0(db)=Louder',
	'Major=1, Minor=0.',
	'1=Exclusively speech, 0=Not exclusively speech',
	'BPM',
	'Ex 4/4, 3/4',
	'1=More positive, 0=More negative']


	avg_df= pd.DataFrame([labels,Q1,avgs,Q3,short_description],index=['type','Q1','Q2','Q3','desc.']).T


	fig, axs = plt.subplots(7,2, figsize=(15, 8),squeeze=False, constrained_layout=True)  # Create a figure and an axes.
	fig.suptitle(f'Stats for Most Played Tracks') #baseline file is in title of plot

	for i in range(len(parameters)):
		if i%2==0:
			axs[math.floor(i/2), 0].set_title(f"{labels[i]}")
			sns.distplot(pd.Series(parameters[i]), hist=True, kde=True, 
				color = 'darkblue', 
				hist_kws={'edgecolor':'black'},
				kde_kws={'linewidth': 3},
				ax=axs[math.floor(i/2), 0])
		else:
			axs[math.floor(i/2), 1].set_title(labels[i])
			#axs[math.floor(i/2), 1].hist(pd.Series(parameters[i]), bins = 20)
			sns.distplot(pd.Series(parameters[i]), hist=True, kde=True, 
				color = 'darkblue', 
				hist_kws={'edgecolor':'black'},
				kde_kws={'linewidth': 3},
				ax=axs[math.floor(i/2), 1])




	html_str = mpld3.fig_to_html(fig)
	Html_file= open("templates/graph.html","w")
	Html_file.write(html_str)
	Html_file.close()

	data=[(x,y) for (x,y) in zip(songs, artists)]

	return data


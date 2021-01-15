import statistics
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import spotipy.util as util
import pandas as pd
import numpy as np
import operator
import math
import constants


client_id = constants.my_client_id
client_secret = constants.my_client_secret
username=constants.my_username

token = util.prompt_for_user_token(username=username, scope='playlist-modify-private,playlist-modify-public,user-library-read, user-top-read', client_id=client_id, client_secret=client_secret, 
	redirect_uri='http://localhost:8080')

sp = spotipy.Spotify(auth=token)

#results = sp.current_user_saved_tracks()
#pprint(results)

def top_four_artists():
    top_tracks=(sp.current_user_top_tracks(limit=50, offset=0, time_range='long_term'))

    artists=[]
    artist_id=[]
    songs=[]
    ids=[]

    for i in top_tracks['items']:
        #pprint(i)
        artists.append(i['artists'][0]['name'])
        artist_id.append(i['artists'][0]['id'])
        songs.append(i['name'])
        ids.append(i['id'])

    artist_list=list(set([(artists[i],artists.count(artists[i]), artist_id[i]) for i in range(len(artists))]))

    sorted_artist_list=(sorted(artist_list, key=lambda x: x[1], reverse=True))[0:4]

    artist_dict={sorted_artist_list[i][0]:(sorted_artist_list[i][2],sp.artist(sorted_artist_list[i][2])['images'][0]['url']) for i in range(len(sorted_artist_list))}
    print(artist_dict)

    return artist_dict

def get_top_tracks(chosen_artist_id):
    results=(sp.artist_top_tracks(chosen_artist_id, country='US'))

    track_titles=[]
    track_uri=[]
    track_image=[]
    for track in results['tracks'][:10]:
        track_titles.append(track['name'])
        track_uri.append(track['uri'])
        track_image.append(track['album']['images'][0]['url'])

    track_dict={track_titles[i]:(track_uri[i],track_image[i]) for i in range(len(track_titles))}

    return(track_dict)


def make_playlist(artist_uri, selected_track_uri):
    #get name and artist of selected track
    selected_track_info=(sp.tracks([selected_track_uri]))

    selected_track=(selected_track_info['tracks'][0]['name'])
    selected_artist=(selected_track_info['tracks'][0]['artists'][0]['name'])





    info= sp.artist_related_artists(artist_uri)

    
    
    similar_artists=[]
    popularity=[]
    uri=[]
    genres=[]

    for i in info['artists']:
        similar_artists.append(i['name'])
        popularity.append(i['popularity'])
        uri.append(i['uri'])

    track_titles=[]
    track_uri=[]
    artist=[]
    track_image=[]
    for i in range(len(uri)):
        results=(sp.artist_top_tracks(uri[i], country='US'))

        for track in results['tracks'][:10]:
            artist.append(similar_artists[i])
            track_titles.append(track['name'])
            track_uri.append(track['uri'])
            track_image.append(track['album']['images'][0]['url'])

    df= pd.DataFrame([artist, track_titles, track_uri], index=['artist','track_titles','track_uri']).T

    print(df)
  
    #get audio parameters from all of the tracks that are by similar artists

    audio_features=[]
    list_of_groups=[]

    for i in range(0, len(track_uri), 100):
        chunk_ids=(track_uri[i:i + 100])
        audio_features.append(sp.audio_features(chunk_ids))

    flat_list = [item for sublist in audio_features for item in sublist]

    print(len(flat_list))

    for item in track_uri:
        audio_features.append(sp.audio_features(item))

    acousticness=([audio_features[i][0]['acousticness'] for i in range(len(track_uri))])
    danceability=([audio_features[i][0]['danceability'] for i in range(len(track_uri))])
    duration_ms=([audio_features[i][0]['duration_ms'] for i in range(len(track_uri))])
    energy=([audio_features[i][0]['energy'] for i in range(len(track_uri))])
    instrumentalness=([audio_features[i][0]['instrumentalness'] for i in range(len(track_uri))])
    key=([audio_features[i][0]['key'] for i in range(len(track_uri))])
    liveness=([audio_features[i][0]['liveness'] for i in range(len(track_uri))])
    loudness=([audio_features[i][0]['loudness'] for i in range(len(track_uri))])
    mode=([audio_features[i][0]['mode'] for i in range(len(track_uri))])
    speechiness=([audio_features[i][0]['speechiness'] for i in range(len(track_uri))])
    tempo=([audio_features[i][0]['tempo'] for i in range(len(track_uri))])
    time_signature=([audio_features[i][0]['time_signature'] for i in range(len(track_uri))])
    valence=([audio_features[i][0]['valence'] for i in range(len(track_uri))])

    df= pd.DataFrame([artist, track_titles, track_uri, acousticness, danceability, duration_ms, energy, instrumentalness, key,
    liveness, loudness, mode, speechiness, tempo, time_signature, valence], 
    index=['artist','track_titles','track_uri', 'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key',
    'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']).T

    print(df)

    #get audio parameters from chosen track
    audio_features=(sp.audio_features(selected_track_uri))
    print(audio_features)
    print(audio_features[0]['liveness'])

    #filter dataframe of similar artist top tracks to only include ones that are similar to the chosen track
    
    df = df[df['danceability']>=.7*(audio_features[0]['danceability'])]
    df = df[df['danceability']<=1.3*(audio_features[0]['danceability'])]

    df = df[df['instrumentalness']>=(audio_features[0]['instrumentalness'])-.1]
    df = df[df['instrumentalness']>=(audio_features[0]['instrumentalness'])-.1]

    df = df[df['energy']>=.5*(audio_features[0]['energy'])]
    df = df[df['energy']<=1.5*(audio_features[0]['energy'])]

    df = df[df['valence']>=.5*(audio_features[0]['valence'])]
    df = df[df['valence']<=1.5*(audio_features[0]['valence'])]

    playlist_name=f"Music like {selected_track} by {selected_artist}"

    sp.user_playlist_create(username, name=playlist_name)

    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:  # iterate through playlists I follow
        if playlist['name'] == playlist_name:  # filter for newly created playlist
            playlist_id = playlist['id']

    df = np.array_split(df, math.ceil(len(df)/100))

    
    for i in df:
        sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=i['track_uri'])

    return(selected_track, selected_artist)


#print(make_playlist('spotify:artist:06HL4z0CvFAxyc27GXpf02','spotify:track:6oVxXO5oQ4pTpO8RSnkzvv'))
# playlist_generators


In order to run this code, you need to create an account with Spotify for Developers at *https://developer.spotify.com/dashboard/login*.
Under the Dashboard tab, click create an app. 

In doing so, you will get a Spotify API client id and client secret. These variables must be input to the constants.py file.

Edit the settings and make the redirect uri 'http://localhost:8080'.

Additionally, you need to get your spotify username which can be found by going to the User page in Spotify, clicking the 3 dots icon --> Share --> Copy Spotify URI. Input this as the username variable in constants.py.

Finally, you will need to be able to fetch Spotify playlist URIs because this is how Spotify can uniquely recognize playlists. To get the URI, go to any playlist, click the 3 dots icon --> Share --> Copy Spotify URI.

# Walking Playlist:
I like to walk to the beat of my music, so I find it frustrating when my music is too fast or too slow to walk to. To remedy this issue, I've created a script that will create the perfect walking playlist every time. The Walking Playlist tab takes in up to 3 existing Spotify playlists, fetches the beats per minute (bpm) of each track, and filters out ones that are not within the optimal walking bpm range. I have found that the optimal bpm range for me is from 110 to 130, but this can vary from person to person. The page takes in a Playlist Name which is the name of the playlist that the app will automatically create. URI 1, 2 and 3 are the playlist URI's of the existing playlists that the user would like to filter for walking music.

![Walking Playlist](/example/walking_playlist.png)



# Similar Songs:
Sometimes people have a song that is the perfect bpm to run, walk, bike, or dance to and they want to find other music that is the same bpm. For instance, Juice by Lizzo is my perfect walking song, so I like to find other songs with its bpm. In order to quickly and easily find more music that is close to the bpm of a certain song, I created the Similar Songs tab. The webpage takes in a Song and Artist which are the track that you think has a good bpm. In my case I would type in Juice and Lizzo in these textboxes. Then the page takes in a URI which is the Spotify playlist that the user will filter for music that is close to the bpm of their input track. Finally the user can use the slider to indicate how lenient they will be with the bpm threshold. The far left of the slider is .5bpm, meaning it will accept songs that are plus or minus .5 bpm of your ideal track, and the far left is 10 bpm so it will accept songs that are plus or minus 10 bpm of your ideal track.

![Similar Songs](/example/similar_songs.png)


# My Likes:
The My Likes tab allows a user to learn more about their music interests. It prompts the user to select if they would like to examine data from their short, medium, or long term listening history. 
![My Likes 1](/example/my_likes1.png)

Upon selection, the probability density functions of different musical features are displayed from their top 50 most listened to tracks of their selected period. These features include tempo, key, energy, and many others.
![My Likes 2](/example/my_likes2.png)

Below, the page displays the artist and track that comprised the top 50 tracks.
![My Likes 3](/example/my_likes3.png)



# New Music:
Sometimes I get in a rut of listening to the same artist on repeat and fail to broaden my musical horizons. To get myself out of this rut, I created the New Music tab which finds music similar to music I like. The page is formatted as a quiz where the first question presents the user with their four most played artists and asks them to pick their favorite. 
![New Music 1](/example/new_music1.png)

Upon selection, the second question appears in which the top 10 tracks of the selected favorite artist are displayed. The user must select their favorite track of those ten tracks, and then the app creates a playlist of music that is by similar artists to the selected favorite artist and is musically similar to the selected favorite track. 
![New Music 2](/example/new_music2.png)


# Graphics: 
While any playlist is being generated, the following gif that I drew is displayed. 
![New Music 2](/static/walk3.gif)



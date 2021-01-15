from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)

app.secret_key ="hello"

@app.route("/") #whatever is in the /<  > is passed into the function as a parameter
def home():
    return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['name'] == '' or request.form['uri1'] == '':
            error = 'Invalid Credentials. Please try again.'
        else:
            playlist_name=request.form['name']
            playlist_list=[]
            playlist_list.append(request.form['uri1'])
            playlist_list.append(request.form['uri2'])
            playlist_list.append(request.form['uri3'])
            playlist_list = list(filter(None, playlist_list))

            from create_new_from_many_playlists import walk_from_many
            walk_from_many(playlist_name, playlist_list)

            return render_template('index.html', error=error)
    return render_template('login.html', error=error)




@app.route("/onesong", methods=['GET', 'POST'])
def onesong():
    error = None
    if request.method == 'POST':
        if request.form['song'] == '' or request.form['artist'] == '':
            error = 'Invalid Credentials. Please try again.'
        else:
            playlist_list=[]
            playlist_list.append(request.form['uri'])
            search_string=f"{request.form['song']} {request.form['artist']}"
            closeness=request.form["name_of_slider"]

            print(closeness)

            from create_new_from_one_song import walk_one_song
            walk_one_song(search_string,playlist_list,float(closeness))

            return render_template('index.html', error=error)

    return render_template('onesong.html', error=error)
    
@app.route("/mylikes", methods=['GET', 'POST'])
def mylikes():
    if request.method == 'POST':
        time_range=request.form['time']


        from plot_my_likes import make_pdf_plot
        data=make_pdf_plot(time_range)
        

        return render_template('mylikes.html', data=data, term=time_range, page=1)

    return render_template('mylikes.html', page=0)


@app.route("/newmusic", methods=['GET', 'POST'])
def newmusic():
    from newmusic import top_four_artists
    session['top_artist_dict']=top_four_artists()
    top_artist_dict=session['top_artist_dict']


    for key in request.form:
        if key.startswith('arti'):
            if request.method == 'POST':
                
                session['artist']=(request.form['artist'])
                print(request.form['artist'])
                
                from newmusic import get_top_tracks
                data=(get_top_tracks(request.form['artist']))

                
                session["top_tracks_dict"] = data
                top_tracks_dict=session["top_tracks_dict"]


                return render_template('newmusic.html', top_artist_dict=top_artist_dict, top_tracks_dict=top_tracks_dict , count=3 )

    for key in request.form:
        if key.startswith('tra'):
            if request.method == 'POST':

                top_tracks_dict=session["top_tracks_dict"]
                
                session["favorite_track"] = (request.form['track'])
                favorite_track=session["favorite_track"]

                artist=session['artist']

                from newmusic import make_playlist
                data=make_playlist(artist,favorite_track)
                

                return render_template('newmusic.html', artist_text=data[1], track_text=data[0], top_artist_dict=top_artist_dict, top_tracks_dict=top_tracks_dict , count=6)
        
    return render_template('newmusic.html', top_artist_dict=top_artist_dict, count=0)



if __name__=="__main__":
    app.run(debug=True)



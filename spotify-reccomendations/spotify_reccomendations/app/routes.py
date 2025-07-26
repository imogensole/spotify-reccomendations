from spotify_reccomendations.app import app
from flask import render_template, redirect, request, session, url_for

from spotify_reccomendations.lib.spotify_auth import SpotifyAuth
from spotify_reccomendations.lib.user_details import SpotifyUser
from spotify_reccomendations.lib.spotify_requests import SpotifyRequests

spotify_auth = SpotifyAuth()


@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template("homepage.html", title="Homepage")


@app.route("/login")
def login():
    auth_url = spotify_auth.auth_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    code = request.args.get('code')
    if code:
        try:
            spotify_auth.handle_auth_callback(code)
            return redirect(url_for('homepage'))
        except Exception as e:
            return f"Authentication failed: {str(e)}", 400
    else:
        return "No authorization code received", 400


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('homepage'))

@app.route("/your_music")
def your_music():
    try:    
        user = SpotifyUser(session["token_info"])
        display_name = user.display_name()
        profile_image = user.profile_image()
        top_tracks = SpotifyRequests(session["token_info"]).user_top_tracks().dataframe.to_dicts()
        return render_template("your_music.html", title="Your Music", display_name=display_name, profile_image=profile_image, top_tracks=top_tracks)
    except Exception as e:
        print(e)
        return redirect(url_for('homepage'))
    

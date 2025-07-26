from spotify_reccomendations.app import app
from flask import render_template, redirect, request, session, url_for
from spotify_reccomendations.spotify_auth import SpotifyAuth


spotify_auth = SpotifyAuth()


@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template("homepage.html", title="Homepage")


@app.route("/login")
def login():
    """Redirect user to Spotify login"""
    auth_url = spotify_auth.get_auth_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    """Handle Spotify OAuth callback"""
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
    """Clear session and logout user"""
    session.clear()
    return redirect(url_for('homepage'))
    

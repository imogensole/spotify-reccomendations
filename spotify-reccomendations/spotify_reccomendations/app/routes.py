from spotify_reccomendations.app import app
from flask import render_template, redirect, request, session, url_for
import json
import re

from spotify_reccomendations.lib.spotify_api.spotify_auth import SpotifyAuth
from spotify_reccomendations.lib.models.user_details import SpotifyUser
from spotify_reccomendations.lib.spotify_api.spotify_requests import SpotifyRequests
from spotify_reccomendations.lib.llm_agent.recommendations_agent import (
    RecommendationsAgent,
)

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
    code = request.args.get("code")
    if code:
        try:
            spotify_auth.handle_auth_callback(code)
            return redirect(url_for("homepage"))
        except Exception as e:
            return f"Authentication failed: {str(e)}", 400
    else:
        return "No authorization code received", 400


@app.route("/logout")
def logout():
    if session:
        session.clear()
        session.modified = True
    return redirect(url_for("homepage"))


@app.route("/your_music")
def your_music():
    if not session.get("token_info"):
        return redirect(url_for("login"))

    try:
        user = SpotifyUser(session["token_info"])
        display_name = user.display_name()
        profile_image = user.profile_image()
        top_tracks = (
            SpotifyRequests(session["token_info"])
            .user_top_tracks()
            .dataframe.to_dicts()
        )
        return render_template(
            "your_music.html",
            title="Your Music",
            display_name=display_name,
            profile_image=profile_image,
            top_tracks=top_tracks,
        )
    except Exception as e:
        print(f"Error in your_music route: {e}")
        session.clear()
        return redirect(url_for("login"))


@app.route("/recommendations")
def recommendations():
    if not session.get("token_info"):
        return redirect(url_for("login"))

    try:
        user = SpotifyUser(session["token_info"])
        top_tracks = SpotifyRequests(session["token_info"]).user_top_tracks()
        recommendations_agent = RecommendationsAgent(user, top_tracks)
        compiled_graph = recommendations_agent.run()
        if user.music_profile is None:
            user.music_profile = recommendations_agent.generate_music_profile(
                compiled_graph
            )
        if user.music_recommendations is None:
            raw_response = recommendations_agent.generate_music_recommendations(
                compiled_graph
            )
            cleaned_response = re.sub(
                r"^```json|```$", "", raw_response.strip(), flags=re.MULTILINE
            ).strip()
            user.music_recommendations = json.loads(cleaned_response)
        
        track_info = SpotifyRequests(session["token_info"]).get_track_info(user.music_recommendations)

    except Exception as e:
        print(f"Error in recommendations route: {e}")
    return render_template(
        "recommendations.html",
        title="Recommendations",
        profile_image=user.profile_image(),
        display_name=user.display_name(),
        music_profile=user.music_profile,
        music_recommendations=track_info.to_dicts()
    )

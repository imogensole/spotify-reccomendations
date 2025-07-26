from app import app

@app.route('/')
@app.route('/home')
def index():
    return "Welcome to the Spotify Reccomendations App"
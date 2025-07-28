# Spotify Recommendations

An AI-powered Spotify dashboard that analyzes your music taste and provides personalized recommendations using LangGraph and OpenAI.

## Demo Video

[!Demo](demo.gif)

View the demo here: https://youtu.be/UHozRJxkQaQ

## 🎵 Features

### Current Features
- **Spotify OAuth Integration**: Secure login with your Spotify account
- **Music Profile Analysis**: AI-generated personality-based music profile using GPT-4
- **Personalized Recommendations**: 10 custom song recommendations based on your top tracks
- **Modern Web Interface**: Clean, responsive design with Spotify-inspired styling
- **Real-time Data**: Fetches your actual Spotify listening data
- **LangGraph Workflow**: Uses LangGraph for structured AI interactions

### Tech Stack
- **Backend**: Flask (Python)
- **AI/ML**: OpenAI GPT-4, LangGraph, LangChain
- **Data Processing**: Polars
- **Authentication**: Spotify Web API OAuth
- **Frontend**: HTML, CSS, Jinja2 Templates

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Spotify Developer Account
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/spotify-reccomendations.git
   cd spotify-reccomendations
   ```

2. **Install dependencies**
   ```bash
   pip install poetry
   poetry install
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   OPENAI_API_KEY=your_openai_api_key
   FLASK_SECRET_KEY=your_flask_secret_key
   ```

4. **Configure Spotify App**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new app
   - Add `http://localhost:5000/callback` to your redirect URIs
   - Copy your Client ID and Client Secret to your `.env` file

### Running the Application

1. **Activate the virtual environment**
   ```bash
   poetry shell
   ```

2. **Run the Flask app**
   ```bash
   poetry run flask run 
   ```

3. **Open your browser**
   Navigate to `http://localhost:5000`

## 📱 Usage

1. **Login**: Click "Login" to authenticate with your Spotify account
2. **View Your Music**: See your top tracks and listening history
3. **Get Recommendations**: Visit the recommendations page to get your AI-generated music profile and personalized song suggestions

## Project Structure

```
spotify-reccomendations/
├── spotify_reccomendations/
│   ├── app/
│   │   ├── routes.py          # Flask routes and views
│   │   └── templates/         # HTML templates
│   ├── lib/
│   │   ├── llm_agent/        # AI recommendation logic
│   │   ├── models/           # Data models
│   │   └── spotify_api/      # Spotify API integration
│   └── spotify_reccomendations.py
├── pyproject.toml
└── README.md
```

## Configuration

### Environment Variables
- `SPOTIFY_CLIENT_ID`: Your Spotify app client ID
- `SPOTIFY_CLIENT_SECRET`: Your Spotify app client secret
- `OPENAI_API_KEY`: Your OpenAI API key
- `FLASK_SECRET_KEY`: Secret key for Flask sessions

### Spotify API Scopes
The app requests the following Spotify scopes:
- `user-top-read`: Access to your top tracks
- `user-read-private`: Access to your profile information

## AI Features

### Music Profile Generation
- Analyzes your top tracks using GPT-4
- Creates a personalized music personality profile
- Identifies patterns in your listening habits

### Recommendation Engine
- Uses LangGraph for structured AI interactions
- Generates 10 personalized song recommendations
- Returns recommendations in JSON format with Spotify track IDs

## 🚧 Development Status

This project is currently a WIP and is actively being updated. New features are being added regularly.

### Planned Features
- [ ] Playlist generation
- [ ] Genre analysis
- [ ] Collaborative filtering
- [ ] Music mood detection
- [ ] Export recommendations to Spotify playlists

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

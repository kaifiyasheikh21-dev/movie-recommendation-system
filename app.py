import streamlit as st
import pickle
import requests
import os
import gdown

# --------------------------
# Ensure artifacts folder exists
# --------------------------
if not os.path.exists('artifacts'):
    os.makedirs('artifacts')

# --------------------------
# File paths
# --------------------------
movie_list_path = 'artifacts/movie_list.pkl'
similarity_path = 'artifacts/similarity.pkl'

# --------------------------
# Direct download URLs from Google Drive
# --------------------------
MOVIE_LIST_URL = 'https://drive.google.com/uc?id=1akk92wYyZ6tZQ8hiVR9jLdvZAfD4E_ki'
SIMILARITY_URL = 'https://drive.google.com/uc?id=1Rz0a658fUb5OWPi73CSO_qmK3EWyGlLo'

# --------------------------
# Download files if they do not exist or are corrupted
# --------------------------
def download_file(url, path):
    if not os.path.exists(path):
        st.info(f"Downloading {os.path.basename(path)}...")
        gdown.download(url, path, quiet=False, fuzzy=True)
    # Quick check if file is a valid pickle
    try:
        with open(path, 'rb') as f:
            pickle.load(f)
    except Exception:
        st.warning(f"{os.path.basename(path)} is corrupted. Redownloading...")
        gdown.download(url, path, quiet=False, fuzzy=True)

download_file(MOVIE_LIST_URL, movie_list_path)
download_file(SIMILARITY_URL, similarity_path)

# --------------------------
# Load data
# --------------------------
with open(movie_list_path, 'rb') as f:
    movies = pickle.load(f)

with open(similarity_path, 'rb') as f:
    similarity = pickle.load(f)

movie_list = movies['title'].values

# --------------------------
# Helper functions
# --------------------------
def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7b51d8779610dadaca77fad2e3781e4d&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "http://image.tmdb.org/t/p/w500" + poster_path
    except:
        pass
    return None

def recommend(movie):
    """Recommend 5 movies similar to the selected movie."""
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movies_name = []
    recommended_movies_poster = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)
        recommended_movies_name.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(poster)
    
    return recommended_movies_name, recommended_movies_poster

# --------------------------
# Streamlit UI
# --------------------------
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Type or select a movie name to get recommendations",
    movie_list
)

if st.button("Show Recommendations"):
    recommended_names, recommended_posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        col.text(recommended_names[idx])
        if recommended_posters[idx]:
            col.image(recommended_posters[idx])
        else:
            col.text("Poster not available")



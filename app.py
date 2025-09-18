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
# Google Drive file URLs
# --------------------------
MOVIE_LIST_URL = "https://drive.google.com/uc?id=1akk92wYyZ6tZQ8hiVR9jLdvZAfD4E_ki"
SIMILARITY_URL = "https://drive.google.com/uc?id=1Rz0a658fUb5OWPi73CSO_qmK3EWyGlLo"

movie_list_path = 'artifacts/movie_list.pkl'
similarity_path = 'artifacts/similarity.pkl'

# --------------------------
# Download files if not present
# --------------------------
def download_file(url, output_path):
    if not os.path.exists(output_path):
        st.info(f"Downloading {os.path.basename(output_path)} from Google Drive...")
        gdown.download(url, output_path, quiet=False, fuzzy=True)
        st.success(f"Downloaded {os.path.basename(output_path)} successfully!")

download_file(MOVIE_LIST_URL, movie_list_path)
download_file(SIMILARITY_URL, similarity_path)

# --------------------------
# Load pickle data safely
# --------------------------
try:
    with open(movie_list_path, 'rb') as f:
        movies = pickle.load(f)
    with open(similarity_path, 'rb') as f:
        similarity = pickle.load(f)
except Exception as e:
    st.error(f"Error loading pickle files: {e}")
    st.stop()

movie_list = movies['title'].values

# --------------------------
# Helper functions
# --------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7b51d8779610dadaca77fad2e3781e4d&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "http://image.tmdb.org/t/p/w500" + poster_path
    except:
        return None
    return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movies_name = []
    recommended_movies_poster = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_name.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    
    return recommended_movies_name, recommended_movies_poster

# --------------------------
# Streamlit UI
# --------------------------
st.header("Movies Recommendation System Using Machine Learning")

selected_movie = st.selectbox(
    'Type or select a movie name to get recommendation',
    movie_list
)

if st.button('Show recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        col.text(recommended_movies_name[idx])
        if recommended_movies_poster[idx]:
            col.image(recommended_movies_poster[idx])
        else:
            col.text("Poster not available")


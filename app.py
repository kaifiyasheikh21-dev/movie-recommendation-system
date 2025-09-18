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
# Download .pkl files from Google Drive if not present
# --------------------------
movie_list_path = 'artifacts/movie_list.pkl'
similarity_path = 'artifacts/similarity.pkl'

if not os.path.exists(movie_list_path):
    gdown.download(
        'https://drive.google.com/uc?id=1akk92wYyZ6tZQ8hiVR9jLdvZAfD4E_ki',
        movie_list_path,
        quiet=False
    )

if not os.path.exists(similarity_path):
    gdown.download(
        'https://drive.google.com/uc?id=1Rz0a658fUb5OWPi73CSO_qmK3EWyGlLo',
        similarity_path,
        quiet=False
    )

# --------------------------
# Load data
# --------------------------
movies = pickle.load(open(movie_list_path, 'rb'))
similarity = pickle.load(open(similarity_path, 'rb'))

movie_list = movies['title'].values

# --------------------------
# Helper functions
# --------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7b51d8779610dadaca77fad2e3781e4d&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "http://image.tmdb.org/t/p/w500" + poster_path
        return full_path
    return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movies_name = []
    recommended_movies_poster = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)
        recommended_movies_poster.append(poster)
        recommended_movies_name.append(movies.iloc[i[0]].title)
    
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


    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])



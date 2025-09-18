import streamlit as st
import pickle
import os
import requests

# Function to download file from Google Drive
def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = None

    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# Paths for local files
os.makedirs("artifacts", exist_ok=True)
movie_list_path = "artifacts/movie_list.pkl"
similarity_path = "artifacts/similarity.pkl"

# Download files if they don't exist
if not os.path.exists(movie_list_path):
    download_file_from_google_drive("1akk92wYyZ6tZQ8hiVR9jLdvZAfD4E_ki", movie_list_path)

if not os.path.exists(similarity_path):
    download_file_from_google_drive("1Rz0a658fUb5OWPi73CSO_qmK3EWyGlLo", similarity_path)

# Load files
movies = pickle.load(open(movie_list_path, 'rb'))
similarity = pickle.load(open(similarity_path, 'rb'))

movie_list = movies['title'].values

st.header("Movies Recommendation System Using Machine Learning")





def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=7b51d8779610dadaca77fad2e3781e4d&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "http://image.tmdb.org/t/p/w500" + poster_path

    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True , key =  lambda x: x[1])
    recommended_movies_name =[]
    recommended_movies_poster = []
    for i in distances[1:6]:
        movie_id =  movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster



st.header("Movies Recommendation System Using Machine Learning")
movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie name to get recommendation',
    movie_list
)

if st.button('Show recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])

    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])

    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])

    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])

    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])


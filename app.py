import pickle
import streamlit as st
import requests

import requests
import urllib.parse

def fetch_poster(movie_name):
    try:
        # Clean movie name for URL
        movie_name = urllib.parse.quote(movie_name)

        url = f"https://api.themoviedb.org/3/search/movie?api_key=7fefe1885f244f5009f9298be95d53a5&query={movie_name}"
        data = requests.get(url).json()

        if data.get('results'):
            for result in data['results']:
                if result.get('poster_path'):
                    return "https://image.tmdb.org/t/p/w500/" + result['poster_path']

        # fallback image
        return "https://via.placeholder.com/300x450?text=No+Image"

    except:
        return "https://via.placeholder.com/300x450?text=Error"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_name = movies.iloc[i[0]].title
        recommended_movie_posters.append(fetch_poster(movie_name))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('🎬 Movies Recommender System')
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

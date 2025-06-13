# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 00:33:14 2025

@author: 91790
"""

import streamlit as st
import pandas as pd
import pickle
import difflib

# Load data and models
movies_data = pd.read_csv('processed_movies.csv')
vectorizer = pickle.load(open('movie_vectorizer.sav', 'rb'))
feature_vectors = pickle.load(open('movie_features.sav', 'rb'))
similarity = pickle.load(open('movie_similarity.sav', 'rb'))

st.title('🎬 Movie Recommendation System')

movie_name = st.text_input('Enter your favourite movie:')

if st.button('Show Recommendations'):

    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

    if find_close_match:
        close_match = find_close_match[0]
        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

        st.subheader('Recommended Movies:')
        i = 1
        for movie in sorted_similar_movies:
            index = movie[0]
            title = movies_data[movies_data.index == index]['title'].values[0]
            if i <= 10:
                st.write(f"{i}. {title}")
                i += 1
    else:
        st.error("No close match found. Try again with a different movie name.")

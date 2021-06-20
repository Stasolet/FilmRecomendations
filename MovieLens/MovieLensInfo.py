import pandas as pd
import os
posters_df = pd.read_csv('MovieLens/movie_poster.csv', header=None, names=['id', 'poster_url'])
posters_df = posters_df.set_index('id')

film_df = pd.read_csv('MovieLens/movie_url.csv', header=None, names=['id', 'movie_url'])
film_df = film_df.set_index('id')


def get_poster_url(film_id: int) -> str:
    try:
        result = posters_df.iloc[film_id].poster_url
    except KeyError:
        result = "broken_poster"
    return result


def get_film_url(film_id: int) -> str:
    try:
        result = film_df.iloc[film_id].movie_url
    except KeyError:
        result = "broken_poster"
    return result

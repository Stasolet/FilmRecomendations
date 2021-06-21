import lenskit.datasets as ds
from lenskit.algorithms import Recommender
from lenskit.algorithms.user_knn import UserUser as KnnUserUser
import pandas as pd
data = ds.ML100K('MovieLens/MovieLensDB/')

user_user = KnnUserUser(nnbrs=100, min_nbrs=20)  # minimum (second) and maximum (first) number of neighbors to consider.
algo = Recommender.adapt(user_user)
algo.fit(data.ratings)


def get_recomendation(ratings: dict, num_recs=10) -> list:
    ratings_seria = pd.Series(ratings)
    ratings_seria.index = list(map(int, ratings_seria.index))
    recs = algo.recommend(-1, num_recs, ratings=ratings_seria)

    joined_data = recs.join(data.movies['title'], on='item')
    return joined_data[['item', 'title']]


def get_multi_recomendations(users_df):

    meaned = users_df.groupby('item').mean('rating')

    return get_recomendation(meaned['rating'], 10000000000000)


def get_films(n: int):
    average_ratings = (data.ratings).groupby(['item']).mean()
    rating_counts = (data.ratings).groupby(['item']).count()
    average_ratings = average_ratings.loc[rating_counts['rating'] > 100]
    sorted_avg_ratings = average_ratings.sort_values(by="rating", ascending=False)
    joined_data = sorted_avg_ratings.join(data.movies['title'], on='item')
    joined_data = joined_data[joined_data.columns[3:]]
    return joined_data.sample(n)
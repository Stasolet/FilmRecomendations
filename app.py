import pandas as pd
from flask import Flask, request
from json import dumps
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, request, session, redirect, json, jsonify
from flask_cors import CORS, cross_origin

from MovieLens.MovieLensInfo import get_poster_url, get_film_url
from MovieLens.RecomendEngine import get_recomendation, get_films, get_multi_recomendations

app = Flask(__name__)
cors = CORS(app)


engine = create_engine(os.getenv("PG_DATABASE_URL").replace("postgres://", "postgresql://", 1))
db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine))
@app.route("/")
@cross_origin()
def hello_world():
    return f'Hello)'


@app.route("/get-films")
@cross_origin()
def get_n_films():
    n = int(request.args.get('n'))
    films = get_films(n)
    result = []
    for row in films.itertuples():
        temp = {'film_id': row.Index, 'film_title': row.title, 'poster_url': get_poster_url(row.Index)}
        result.append(temp)
    return {'films': result}


@app.route("/davaaaaay", methods=["POST", "GET"])
@cross_origin()
def add_user():
    data = request.get_json()
    username = data['username']
    ratings = data['ratings']
    friends = data['friends']
    recs = None
    if not ratings:
        return None
    if friends:
        users = db.execute(f'select "user_id", "film_id", "rating" from "rating" where "user_id" in({", ".join(map(str, friends))}) ORDER BY "user_id";').fetchall()
        users_df = pd.DataFrame(users, columns=["user", "item", "rating"])
        recs = get_multi_recomendations(users_df)
    else:
        recs = get_recomendation(ratings)
    db.execute('INSERT INTO "user" ("username") VALUES ( :username )', {"username": username})
    user_id = db.execute('select "id" from "user" where "username" = :username ORDER BY id DESC LIMIT 1;',
                         {'username': username}).fetchall()[0][0]
    for film_id in ratings.keys():
        db.execute('INSERT INTO "rating" ("user_id", "film_id", "rating") VALUES ( :user_id, :film_id, :rating)',
                   {"user_id": user_id, "film_id": film_id, "rating": ratings[film_id]})
    db.commit()
    if recs is None:
        return "no way"
    recs: pd.DataFrame
    result = []
    for row in recs.itertuples():
        temp = {'film_id': row.Index, 'film_title': row.title, 'poster_url': get_poster_url(row.item)}
        result.append(temp)
    return {'films': result[:28]}


@app.route("/get_users")
@cross_origin()
def get_users():
    users = db.execute('select "id", "username" from "user" ORDER BY id DESC;').fetchall()
    result = [{'user_id': r[0], 'username': r[1]} for r in users]
    return {'friends': result}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

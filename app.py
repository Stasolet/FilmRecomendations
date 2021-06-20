import pandas as pd
from flask import Flask, request
from json import dumps
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, request, session, redirect, json, jsonify
from flask_cors import CORS, cross_origin

from MovieLens.MovieLensInfo import get_poster_url, get_film_url
from MovieLens.RecomendEngine import get_recomendation, get_films

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def hello_world():
    return f'Hello)'


@app.route("/get_films")
def get_n_films():
    n = int(request.args.get('n'))
    films = get_films(n)
    result = []
    for row in films.itertuples():
        temp = {'film_id': row.Index, 'film_title': row.title, 'poster_url': get_poster_url(row.Index)}
        result.append(temp)
    return {'films': result}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

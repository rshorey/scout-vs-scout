from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

def get_phrase_count(phrase,state):
    sunlight_api_key = os.environ.get("SUNLIGHT_API_KEY")
    base_url = "http://capitolwords.org/api/1/text.json?apikey={api_key}&start_date=2014-01-01&end_date=2014-12-31".format(api_key=sunlight_api_key)
    if state is not None:
        base_url += "&state={state}".format(state=state.upper())
    query_url = base_url + "&phrase={query}".format(query=phrase.replace(" ","+"))
    query_result = requests.get(query_url).json()
    return query_result["num_found"]

@app.route('/')
@app.route('/<state>')
def index(state=None):
    boy_mentions = get_phrase_count("boy scouts",state)
    girl_mentions = get_phrase_count("girl scouts",state)
    eagle_mentions = get_phrase_count("eagle scout",state)
    gold_mentions = get_phrase_count("gold award",state)
    return render_template('index.html',
                            boy_mentions=boy_mentions,
                                girl_mentions=girl_mentions)
if __name__ == '__main__':
    app.run(debug=True)

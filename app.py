from flask import Flask
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
    return ('Boy Scouts mentions: {boy_mentions}<br>'\
        'Girl Scouts mentions: {girl_mentions}<br>'\
        'Eagle Scout mentions: {eagle_mentions}<br>'\
        'Gold Award mentions: {gold_mentions}<br>').format(boy_mentions=boy_mentions,
                                girl_mentions=girl_mentions,
                                eagle_mentions=eagle_mentions,
                                gold_mentions=gold_mentions)

if __name__ == '__main__':
    app.run(debug=True)

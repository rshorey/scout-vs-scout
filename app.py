from flask import Flask
import requests
import os

app = Flask(__name__)

@app.route('/')
@app.route('/<state>')
def index(state=None):
    sunlight_api_key = os.environ.get("SUNLIGHT_API_KEY")
    base_url = "http://capitolwords.org/api/1/text.json?apikey={api_key}&start_date=2014-01-01&end_date=2014-12-31".format(api_key=sunlight_api_key)
    if state is not None:
        base_url += "&state={state}".format(state=state.upper())
    boy_scouts_url = base_url + "&phrase=boy+scouts"
    girl_scouts_url = base_url + "&phrase=girl+scouts"
    boy_page = requests.get(boy_scouts_url).json()
    girl_page = requests.get(girl_scouts_url).json()
    boy_mentions = boy_page["num_found"]
    girl_mentions = girl_page["num_found"]
    return 'Boy Scout mentions: {boy_mentions} Girl Scout mentions: {girl_mentions}'.format(boy_mentions=boy_mentions,girl_mentions=girl_mentions)

if __name__ == '__main__':
    app.run(debug=True)

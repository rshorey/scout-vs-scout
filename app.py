from flask import Flask, render_template, request, redirect
import requests
import os
import datetime

app = Flask(__name__)

def get_phrase_count(phrase,state):
    sunlight_api_key = os.environ.get("SUNLIGHT_API_KEY")
    now = datetime.datetime.now()
    one_year = now - datetime.timedelta(days=365)
    end_date = now.strftime("%Y-%m-%d")
    start_date = one_year.strftime("%Y-%m-%d")
    base_url = "http://capitolwords.org/api/1/text.json?apikey={api_key}&start_date={start_date}&end_date={end_date}"
    base_url = base_url.format(api_key=sunlight_api_key,start_date=start_date,end_date=end_date)
    if state is not None:
        base_url += "&state={state}".format(state=state.upper())
    query_url = base_url + "&phrase={query}".format(query=phrase.replace(" ","+"))
    query_result = requests.get(query_url).json()
    return query_result["num_found"]

def get_leg(zipcode):
    sunlight_api_key = os.environ.get("SUNLIGHT_API_KEY")
    base_url = "https://congress.api.sunlightfoundation.com/legislators/locate"
    query_url = base_url + "?apikey={apikey}&zip={zipcode}".format(apikey=sunlight_api_key,zipcode=zipcode)
    results = requests.get(query_url).json()
    members = {"house":[],"senate":[]}
    for mem in results["results"]:
        name_parts = [mem["title"],
                        mem["first_name"],
                        mem["middle_name"],
                        mem["last_name"],
                        mem["name_suffix"]
                    ]
        name = " ".join([n for n in name_parts if n])
        members[mem["chamber"]].append({
            "name":name,
            "email":mem["oc_email"],
            "address":mem["office"],
            "twitter":mem.get("twitter",None)
            })

    return members

@app.route('/')
def index(state=None):
    boy_mentions = get_phrase_count("boy scouts",state)
    girl_mentions = get_phrase_count("girl scouts",state)
    eagle_mentions = get_phrase_count("eagle scout",state)
    gold_mentions = get_phrase_count("gold award",state)
    return render_template('index.html',
                            boy_mentions=boy_mentions,
                                girl_mentions=girl_mentions)

@app.route('/getzip', methods = ['POST'])
def signup():
    zipcode = request.form['zipcode']
    return redirect('/contact/{}'.format(zipcode))

@app.route('/contact/<zipcode>')
def contact(zipcode):
    members = get_leg(zipcode)
    boy_mentions = get_phrase_count("boy scouts",None)
    girl_mentions = get_phrase_count("girl scouts",None)
    return render_template('contact.html',members=members,
                                        boy_mentions=boy_mentions,
                                        girl_mentions=girl_mentions)


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

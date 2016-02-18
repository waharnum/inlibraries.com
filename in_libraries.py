from flask import Flask
from flask import render_template
from flask import request
from datetime import date
from random import randint
import json

app = Flask(__name__)

# Load synonyms
synonyms_json = open("synonyms.json").read()
synonyms = json.loads(synonyms_json)

# part = part of speech (noun, verb, etc)
# word = specific word to get a synonym for
def get_synonym(part, word):
    synonyms_for_word = synonyms[part][word]
    random_number = randint(0, len(synonyms_for_word)-1)
    return synonyms_for_word[random_number]

# Set up Jinja tags
app.jinja_env.globals.update(synonym=get_synonym)

@app.route('/')
def front_page(subdomain=None):
    subdomain_split = request.host.split(".")[0].split("_")
    subdomain = " ".join(subdomain_split)
    subdomain_title = subdomain.title()
    year = date.today().year
    return render_template('front_page.html', subdomain=subdomain, subdomain_title=subdomain_title, year=year)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

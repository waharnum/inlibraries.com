from flask import Flask
from flask import render_template
from flask import request
from datetime import date
from random import randint

app = Flask(__name__)

# TODO: remove before production
app.debug = True

# Set up Jinja tags



def get_synonym_leadership():
    synonyms_leadership = ["leadership", "administration", "management"]
    random_number = randint(0, len(synonyms_leadership)-1)
    return synonyms_leadership[random_number]
    return u'leadership'

app.jinja_env.globals.update(synonym_leadership=get_synonym_leadership)

@app.route('/')
def front_page(subdomain=None):
    subdomain_split = request.host.split(".")[0].split("_")
    subdomain = " ".join(subdomain_split)
    subdomain_title = subdomain.title()
    year = date.today().year
    return render_template('front_page.html', subdomain=subdomain, subdomain_title=subdomain_title, year=year)

if __name__ == '__main__':
    app.run()

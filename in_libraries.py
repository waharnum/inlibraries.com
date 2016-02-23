from flask import Flask
from flask import render_template
from flask import render_template_string
from flask import request
from datetime import date
from random import randint
import json

app = Flask(__name__)

# TODO: remove before production
app.debug = True

# Load synonyms
synonyms_json = open("synonyms.json").read()
synonyms = json.loads(synonyms_json)

# Load session madlibs
session_madlibs_json = open("session_madlibs.json").read()
session_madlibs = json.loads(session_madlibs_json)

# Load image information
image_json = open("images.json").read()
images_information = json.loads(image_json)

def get_random_image():
    random_number = randint(0, len(images_information)-1)
    return images_information[random_number]

# part = part of speech (noun, verb, etc)
# word = specific word to get a synonym for
# refer to synonyms.json
def get_synonym(part, word):
    synonyms_for_word = synonyms[part][word]
    random_number = randint(0, len(synonyms_for_word)-1)
    return synonyms_for_word[random_number]

# Set up Jinja tag for synonym usage in templates
app.jinja_env.globals.update(synonym=get_synonym)

# Set up Jinja tag for random image filename in template
app.jinja_env.globals.update(random_image=get_random_image)

# Front page route
@app.route('/')
def front_page(subdomain=None):
    subdomain_split = request.host.split(".")[0].split("_")
    subdomain = " ".join(subdomain_split)
    subdomain_title = subdomain.title()
    year = date.today().year

    # Set to True to dump all the madlibs - good for testing
    test_session_madlibs = False

    def get_random_session_madlib():
        random_number = randint(0, len(session_madlibs)-1)
        return get_session_madlib(random_number)

    def get_random_session_madlibs(count=3):
        sessions = []

        for i in range(0, count):
            session = get_random_session_madlib()
            # If this is an exact duplicate, keep regenerating until it's not
            while session in sessions:
                session = get_random_session_madlib()
            sessions.append(session)

        return sessions

    def get_session_madlib(idx):
        template_string = session_madlibs[idx]
        return render_template_string(template_string, subdomain=subdomain, subdomain_title=subdomain_title, year=year)

    # Set up Jinja tag for random session madlib in templates
    app.jinja_env.globals.update(random_sessions=get_random_session_madlibs)

    app.jinja_env.globals.update(session_by_index=get_session_madlib)

    return render_template('front_page.html', subdomain=subdomain, subdomain_title=subdomain_title, year=year, test_session_madlibs=test_session_madlibs, session_madlibs=session_madlibs)

if __name__ == '__main__':
    app.run()

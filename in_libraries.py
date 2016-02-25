from flask import Flask
from flask import render_template
from flask import render_template_string
from flask import request
from flask import Response
from datetime import date
from random import randint
import json

APP = Flask(__name__)

# TODO: remove before production
APP.debug = True

# loads a JSON file to a dictionary variable
def dict_from_json_file(json_file_path):
    json_file = open(json_file_path).read()
    return json.loads(json_file)

# Load synonyms
SYNONYMS = dict_from_json_file("synonyms.json")

# Load session madlibs
SESSION_MADLIBS = dict_from_json_file("session_madlibs.json")

# Load speaker madlibs
SPEAKER_MADLIBS = dict_from_json_file("speaker_madlibs.json")

# Load image information
IMAGES_INFORMATION = dict_from_json_file("images.json")

# Load gradients
WHITE_TEXT_GRADIENTS = dict_from_json_file("white_text_gradients.json")

# gets a random item from a collection and returns it
def get_random_from_list(collection):
    random_number = randint(0, len(collection)-1)
    return collection[random_number]

# part = part of speech (noun, verb, etc)
# word = specific word to get a synonym for
# refer to synonyms.json
def get_synonym(part, word):
    synonyms_for_word = SYNONYMS[part][word]
    return get_random_from_list(synonyms_for_word)

def get_session_madlib(template_string, subdomain, year):
    return render_template_string(template_string, subdomain=subdomain, subdomain_title=subdomain.title(), year=year)

def get_speaker_madlib(template_string):
    speaker_first_name = get_synonym("concepts", "first_names")
    speaker_last_name = get_synonym("concepts", "last_names")
    return render_template_string(template_string, speaker_first_name=speaker_first_name, speaker_last_name=speaker_last_name)

def get_random_speaker_madlib():
    speaker_template = get_random_from_list(SPEAKER_MADLIBS)
    return get_speaker_madlib(speaker_template)

def get_speaker_madlib_by_index(idx):
    speaker_template = SPEAKER_MADLIBS[idx]
    return get_speaker_madlib(speaker_template)

def get_random_speaker_madlibs(count=3):
    speakers = []

    for i in range(0, count):
        speaker = get_random_speaker_madlib()
        # If this is an exact duplicate, keep regenerating until it's not
        while speaker in speakers:
            speaker = get_random_speaker()
        speakers.append(speaker)

    return speakers

def get_random_image():
    return get_random_from_list(IMAGES_INFORMATION)

def get_random_white_text_gradient():
    return get_random_from_list(WHITE_TEXT_GRADIENTS)

# Set up Jinja tag for synonym usage in templates
APP.jinja_env.globals.update(synonym=get_synonym)

# Set up Jinja tag for random speaker generation
APP.jinja_env.globals.update(random_speaker=get_random_speaker_madlib)

# Set up Jinja tag for speaker by index
APP.jinja_env.globals.update(speaker_by_index=get_speaker_madlib_by_index)

# Set up Jinja tag for random speaker group generation
APP.jinja_env.globals.update(random_speakers=get_random_speaker_madlibs)

# Set up Jinja tag for random image filename in template
APP.jinja_env.globals.update(random_image=get_random_image)

# Set up Jinja tag for random white text gradient background in template
APP.jinja_env.globals.update(random_white_text_gradient=get_random_white_text_gradient)

# Front page route
@APP.route('/')
def front_page(subdomain=None):
    subdomain_raw = request.host.split(".")[0]
    subdomain_split = subdomain_raw.split("_")
    subdomain_underscores_converted = " ".join(subdomain_split)
    subdomain_double_hyphens_converted = " ".join(subdomain_underscores_converted.split("--"))
    print(subdomain_double_hyphens_converted)
    subdomain = subdomain_double_hyphens_converted
    subdomain_title = subdomain_double_hyphens_converted.title()
    year = date.today().year

    # Set to True to dump all the madlibs - good for testing
    test_mode = False

    def get_random_session_madlib():
        session_template = get_random_from_list(SESSION_MADLIBS)
        return get_session_madlib(session_template, subdomain, year)

    def get_session_madlib_by_index(idx):
        session_template = SESSION_MADLIBS[idx]
        return get_session_madlib(session_template, subdomain, year)

    def get_random_session_madlibs(count=3):
        sessions = []

        for i in range(0, count):
            session = get_random_session_madlib()
            # If this is an exact duplicate, keep regenerating until it's not
            while session in sessions:
                session = get_random_session_madlib()
            sessions.append(session)

        return sessions

    # Set up Jinja tag for random session madlib in templates
    APP.jinja_env.globals.update(random_sessions=get_random_session_madlibs)

    APP.jinja_env.globals.update(session_by_index=get_session_madlib_by_index)

    return render_template('front_page.html', subdomain_raw=subdomain_raw, subdomain=subdomain, subdomain_title=subdomain_title, year=year, test_mode=test_mode, session_madlibs=SESSION_MADLIBS, speaker_madlibs=SPEAKER_MADLIBS)

@APP.route('/css/random.css')
def random_css():
    css = render_template('random.css')
    return Response(css, mimetype='text/css')

if __name__ == '__main__':
    APP.run()

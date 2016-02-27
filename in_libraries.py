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

def get_random_speaker_madlibs(count=3):
    speakers = []

    for i in range(0, count):
        speaker = get_random_speaker_madlib()
        # If this is an exact duplicate, keep regenerating until it's not
        while speaker in speakers:
            speaker = get_random_speaker_madlib()
        speakers.append(speaker)

    return speakers

def get_all_speaker_madlibs():
    speakers = []

    for speaker_template in SPEAKER_MADLIBS:
        speaker = get_speaker_madlib(speaker_template)
        speakers.append(speaker)
    return speakers

# Set up Jinja tag for synonym usage in templates
APP.jinja_env.globals.update(synonym=get_synonym)

# Conference request object
class ConferenceRequest:
    def __init__(self, request):
        self.subdomain = request.host.split(".")[0]
        subdomain_split = self.subdomain.split("_")
        subdomain_underscores_converted = " ".join(subdomain_split)
        subdomain_double_hyphens_converted = " ".join(subdomain_underscores_converted.split("--"))
        self.subdomain_as_string = subdomain_double_hyphens_converted
        self.year = date.today().year

    def get_random_session_madlib(self):
        session_template = get_random_from_list(SESSION_MADLIBS)
        return get_session_madlib(session_template, self.subdomain_as_string, self.year)

    def get_random_session_madlibs(self, count=3):
        sessions = []

        for i in range(0, count):
            session = self.get_random_session_madlib()
            # If this is an exact duplicate, keep regenerating until it's not
            while session in sessions:
                session = self.get_random_session_madlib()
            sessions.append(session)

        return sessions

    def get_all_session_madlibs(self):
        sessions = []

        for session_template in SESSION_MADLIBS:
            session = get_session_madlib(session_template, self.subdomain_as_string, self.year)
            sessions.append(session)

        return sessions

# Front page route
@APP.route('/')
def front_page(subdomain=None):
    conference_request = ConferenceRequest(request)

    subdomain = conference_request.subdomain_as_string
    subdomain_raw = conference_request.subdomain
    subdomain_title = conference_request.subdomain_as_string.title()
    year = conference_request.year

    # Set to True to dump all the madlibs etc - good for testing
    test_mode = False

    random_strip_image = get_random_from_list(IMAGES_INFORMATION)

    if(test_mode):
        speakers = get_all_speaker_madlibs()
        sessions = conference_request.get_all_session_madlibs()
    else:
        speakers = get_random_speaker_madlibs()
        sessions = conference_request.get_random_session_madlibs()

    return render_template('front_page.html', subdomain_raw=subdomain_raw, subdomain=subdomain, subdomain_title=subdomain_title, year=year, test_mode=test_mode, sessions=sessions, speakers=speakers, random_strip_image=random_strip_image)

@APP.route('/css/random.css')
def random_css():
    dark_gradient_background = get_random_from_list(WHITE_TEXT_GRADIENTS)
    css = render_template('random.css', dark_gradient_background=dark_gradient_background)
    return Response(css, mimetype='text/css')

if __name__ == '__main__':
    APP.run()

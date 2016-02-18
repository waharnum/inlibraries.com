from flask import Flask
from flask import render_template
from flask import request
from datetime import date

app = Flask(__name__)

@app.route('/')
def front_page(subdomain=None):
    subdomain_split = request.host.split(".")[0].split("_")
    subdomain = " ".join(subdomain_split)
    subdomain_title = subdomain.title()
    year = date.today().year
    return render_template('front_page.html', subdomain=subdomain, subdomain_title=subdomain_title, year=year)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

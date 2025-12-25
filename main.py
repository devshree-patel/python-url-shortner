import random
import string
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
shortened_urls = {}


def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


@app.route('/', methods=['GET', 'POST'])
def index():
    short_link = None

    if request.method == 'POST':
        long_url = request.form['long_url']

        if not long_url.startswith(('http://', 'https://')):
            long_url = 'https://' + long_url

        short_url = generate_short_url()
        while short_url in shortened_urls:
            short_url = generate_short_url()

        shortened_urls[short_url] = long_url
        short_link = request.url_root + short_url

    return render_template("index.html", short_link=short_link)


@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404


if __name__ == "__main__":
    app.run(debug=True)

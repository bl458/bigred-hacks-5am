from flask import Flask, render_template
import data_fetcher
from werkzeug.contrib.cache import SimpleCache
import json

cache = SimpleCache()
app = Flask(__name__)

@app.route("/")
def index():
    # return ''.join('{}{}'.format(key, val) for key, val in sorted(data_fetcher.main().items()))
    id = 'homepage'
    value = cache.get(id)
    electricity=data_fetcher.main()
    if value is not None:
        print "used cache -----------------------------"
        return value
    print 'no cache ------------------------'
    value = render_template('index.html', electricity=electricity)
    cache.set(id, value, timeout=60 * 5)
    return value

if __name__ == "__main__":
    app.run()

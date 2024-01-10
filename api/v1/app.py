#!/usr/bin/python3
"""
    Flask application
"""


from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)
host = os.environ.get("HBNB_API_HOST", "0.0.0.0")

@app.teardown_appcontext
def tear_down():
    """Clean up resources"""
    storage.close()


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = os.environ.get("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)

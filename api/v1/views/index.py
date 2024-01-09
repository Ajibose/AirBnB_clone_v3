#!/usr/bin/python3
"""
    Create Blueprint routes
"""
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Testing flask"""
    return jsonify({"status": "OK")

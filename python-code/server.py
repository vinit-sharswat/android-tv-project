# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 16:18:49 2021

@author: chirpy.coders
@Description: Endpoints to pull the video details from the database and return to the client side
"""

from flask import Flask, jsonify, request

import time

port = 8000  # Dev

app = Flask(__name__, static_url_path='/public')


# This function calculates the currentTime and returns back in milliseconds
def current_milli_time(): return round(time.time() * 1000)


# This endpoint takes the following input: {"tv_index": "tv_index_value","previous_video_index": "video_index_value"}
@app.route("/get-video", methods=['POST'])
def get_video():
    inputData = request.get_json()

    if(not inputData["previous_video_index"]):
        print("{}: User connection has been established: Play First video".format(
            inputData["tv_index"]))
    else:
        print("{}: User looking for a new video".format(
            inputData["tv_index"]))

    resp = jsonify({"Success": "tv_video_path"})
    resp.status_code = 500
    return resp


@app.route('/healthz')
def hello_world():
    resp = jsonify({"Status": "UP"})
    resp.status_code = 404
    return resp


@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    resp = jsonify({"Error": "Endpoint not found: " + request.url})
    resp.status_code = 404
    return resp


@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    resp = jsonify({"Error": "Error Detected: " + request.url})
    resp.status_code = 500
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, threaded=True)
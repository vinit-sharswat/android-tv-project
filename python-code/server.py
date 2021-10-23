# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 16:18:49 2021

@author: chirpy.coders
@Description: Endpoints to pull the video details from the database and return to the client side
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from cloudant.client import Cloudant
from cloudant.query import Query

serviceUsername = os.environ['serviceUsername']
servicePassword = os.environ['servicePassword']
serviceURL = os.environ['serviceURL']
# serviceUsername = "apikey-v2-2zqrhw30ux33awo5j9anua3hr69rirt1xlflkyvh1euf"
# servicePassword = "3185eb6c4f9b49b030999455621d62ce"
# serviceURL = "https://apikey-v2-2zqrhw30ux33awo5j9anua3hr69rirt1xlflkyvh1euf:3185eb6c4f9b49b030999455621d62ce@50a7b96e-13aa-41ca-8020-992577e71d7a-bluemix.cloudantnosqldb.appdomain.cloud"

client = Cloudant(serviceUsername, servicePassword, url=serviceURL)

port = 8000  # Dev

app = Flask(__name__)
CORS(app)


# This endpoint takes the following input: {"tv_index": "tv_index_value","previous_video_index": "video_index_value"}
@app.route("/fetch", methods=['POST'])
def fetch():
    print("Video Fetch API is hit")
    try:
        inputData = request.get_json()

        if(not inputData["previous_video_index"]):
            print("{}: User connection has been established: Play First video".format(
                inputData["tv_index"]))
        else:
            print("{}: User looking for a new video".format(
                inputData["tv_index"]))

        output = query_database({
            "selector": {
                "tv_index": inputData["tv_index"]
            },
            "fields": [
                "next_video_path",
                "video_loop_path"
            ]
        })
        resp = jsonify({
            "success": True,
            "next_video_path": output[0]["next_video_path"],
            "video_loop_path": output[0]["video_loop_path"]
        })
        resp.status_code = 200
        return resp
    except Exception as e:
        print("Error: ", e)
        resp = jsonify({"success": False})
        resp.status_code = 500
        return resp


@app.route('/healthz')
def hello_world():
    resp = jsonify({"Status": "UP"})
    resp.status_code = 200
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


def query_database(query):
    client.connect()
    my_database = client['tvs']

    queryOutput = Query(
        my_database, selector=query["selector"], fields=query["fields"])

    output = queryOutput(limit=1)['docs']
    client.disconnect()
    return output


if __name__ == '__main__':
    # Debug/Development
    app.run(host="0.0.0.0", port=os.environ['PORT'])
    # Production
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()

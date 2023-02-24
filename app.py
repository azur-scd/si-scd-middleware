from flask import Flask, jsonify, abort, render_template,url_for,request,session, redirect, send_from_directory, Response, Blueprint
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import Api, swagger, Schema
from flask_json import FlaskJSON, json_response
from flask_cors import CORS
import pandas as pd
import requests
import json
from dotenv import dotenv_values

env = dotenv_values(".env")

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

port = env['APP_PORT']
host = env['APP_HOST']
api_version = env['API_VERSION']
url_subpath = env['URL_SUBPATH']
si_api_horaires = env["SI_API_HOARIRES"]

# It dynamically adapts Flask converted url of static files (/sttaic/js...) + templates html href
# links according to the url app path after the hostname (set in cnfig.py)
class ReverseProxied(object):
    def __init__(self, app, script_name=None, scheme=None, server=None):
        self.app = app
        self.script_name = script_name
        self.scheme = scheme
        self.server = server

    def __call__(self, environ, start_response):
        if (
            script_name := environ.get('HTTP_X_SCRIPT_NAME', '')
            or self.script_name
        ):
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        if scheme := environ.get('HTTP_X_SCHEME', '') or self.scheme:
            environ['wsgi.url_scheme'] = scheme
        if server := environ.get('HTTP_X_FORWARDED_SERVER', '') or self.server:
            environ['HTTP_HOST'] = server
        return self.app(environ, start_response)

FlaskJSON(app)
api = Api(app, title='SCD-UCA Middleware SI SCD', api_version='1.0', api_spec_url='/api/swagger', base_path=f'{host}:{port}')
app.wsgi_app = ReverseProxied(app.wsgi_app, script_name=url_subpath)

@api.representation('application/json')
def output_json(data, code):
    return json_response(data_=data, status_=code)

class HelloWorld(Resource):
    def get(self):
        # Default to 200 OK
        return jsonify({'msg': 'Hello world'})

# It takes a biblio_id as input, and returns a list of items associated with that biblio_id
class Horaires(Resource):

    @swagger.doc({
    })

    def get(self):
        url = si_api_horaires
        response = requests.request("GET", url).text
        data = json.loads(response)      
        return jsonify(data)

api.add_resource(HelloWorld, f'/api/{api_version}', f'/api/{api_version}/hello')      
api.add_resource(Horaires, f'/api/{api_version}/horaires')

if __name__ == '__main__':
    app.run(debug=True,port=port,host=host)
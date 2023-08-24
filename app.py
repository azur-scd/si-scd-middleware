from flask import Flask, jsonify, make_response, Response, abort, render_template,url_for,request,session, redirect, send_from_directory, Response, Blueprint
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import Api, swagger, Schema
from flask_json import FlaskJSON, json_response
from flask_cors import CORS
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from json2xml import json2xml
from json2xml.utils import readfromurl
import subprocess
from dotenv import dotenv_values

env = dotenv_values(".env")

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

port = env['APP_PORT']
host = env['APP_HOST']
api_version = env['API_VERSION']
url_subpath = env['URL_SUBPATH']
si_api_horaires = env["SI_API_HORAIRES"]
si_api_bdd = env["SI_API_BDD"]

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

@api.representation('application/xml')
def output_xml(data, code):
    return make_response(data_=data, status_=code)

def _extracted_from_get_7(arg0, arg1):
        response = make_response(arg0)
        response.headers["Content-Type"] = arg1
        return response

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
    
class OaiProtocol(Resource):
    def get(self):
        return True
    
class OaiProtocol(Resource):
    def get(self):
        return _extracted_from_get_7("true", "text/html")
    
class OaiBdd(Resource):
    def get(self):  # sourcery skip: avoid-builtin-shadow
        # the url parameters are unused for the moment but who knows in teh future ?
        #verb = request.args.get('verb')
        #metadataPrefix = request.args.get('metadataPrefix')
        #data = {"verb": verb, "metadataPrefix": metadataPrefix, "set": set}
        if ('verb' in request.args) & (request.args.get('verb') == "Identify"):
            with open("oai_bdd_files/identify.xml","r", encoding='utf-8') as f:
                xml_oai = f.read()
                return _extracted_from_get_7(xml_oai, "application/xml")
        else:
            set = request.args.get('set')
            if set == "BDD":
                data = readfromurl(si_api_bdd)
                xml = json2xml.Json2xml(data, wrapper="Resources", pretty=True).to_xml()
                with open("oai_bdd_files/bdd.xml","w", encoding='utf-8') as xml_file:
                    xml_file.write(xml)
                subprocess.run(['/bin/bash','./run_saxon.sh','oai_bdd_files/si2oai.xsl','oai_bdd_files/bdd.xml','oai_bdd_files/bdd_result.xml'])
                with open("oai_bdd_files/bdd_result.xml","r", encoding='utf-8') as f:
                    xml_result = f.read()
                    return _extracted_from_get_7(xml_result, "application/xml")

api.add_resource(HelloWorld, f'/api/{api_version}', f'/api/{api_version}/hello')   
api.add_resource(Horaires, f'/api/{api_version}/horaires')   
api.add_resource(OaiProtocol, '/oai&protocol=OAI')
api.add_resource(OaiBdd, '/oai')

if __name__ == '__main__':
    app.run(debug=True,port=port,host=host)
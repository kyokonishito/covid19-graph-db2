from flask import Flask, request
import os
from os.path import join, dirname
from dotenv import load_dotenv
from db2data import Db2dataTool

app = Flask(__name__, static_url_path='')
if os.getenv('APP_CONFIG_FILE'):
    app.config.from_envvar('APP_CONFIG_FILE')

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

if os.environ.get("FLASK_CONFIG") == "DEV":
    app.config.from_object('config.debug')
else:
    app.config.from_object('config.default')
    

db2info = {}
db2info['DBNAME']= os.environ.get("DBNAME");
db2info['USERID']= os.environ.get("USERID");
db2info['PASSWD']= os.environ.get("PASSWD");
db2info['URL']= os.environ.get("URL");
db2info['CRN']= os.environ.get("CRN");
   
@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/getdata', methods=['POST'])
def getData():
    req = request.json
    todate = req.get("todate")
    fromdate = req.get("fromdate")
    db2data = Db2dataTool(db2info)
    response = db2data.getData(fromdate, todate) 
    return response

@app.after_request
def apply_caching(response):
    if os.environ.get("FLASK_CONFIG") == "DEV":  #add CORS only DEV mode
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == "__main__":
    if app.config["HOST"]:
        app.run(debug=app.config["DEBUG"], host='0.0.0.0', port=app.config["PORT"], threaded=True)
    else:
        app.run(debug=app.config["DEBUG"], port=app.config["PORT"], threaded=True)
import sys
import simplejson as json
import mariadb
import os
import flask
from flask import request
from flask import Blueprint
from dotenv import load_dotenv

load_dotenv()

airlines = Blueprint('airlines', __name__)

config = {
    'host': os.getenv("DB_HOST"),
    'port': int(os.getenv("DB_PORT")),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASS"),
    'ssl': True
}

@airlines.route('/api/airlines', methods=['GET'])
def index():
   conn = mariadb.connect(**config)
   cur = conn.cursor()
   cur.execute("select * from travel.airlines order by airline")
   row_headers=[x[0] for x in cur.description] 
   rv = cur.fetchall()
   json_data=[]
   for result in rv:
        json_data.append(dict(zip(row_headers,result)))
   
   return json.dumps(json_data)
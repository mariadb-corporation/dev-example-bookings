import sys
import simplejson as json
from datetime import datetime
import decimal
import mariadb
import os
import flask
from flask import request
from flask import Blueprint
from dotenv import load_dotenv

load_dotenv()

flights = Blueprint('flights', __name__)

config = {
    'host': os.getenv("DB_HOST"),
    'port': int(os.getenv("DB_PORT")),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASS"),
    'ssl': True
}

def converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

@flights.route('/api/flights', methods=['GET'])
def index():
   date_str = request.args.get('dt')
   origin = request.args.get('o')
   dest = request.args.get('d')
   date = datetime.strptime(date_str, '%Y-%m-%d')
   year = date.year
   month = date.month
   day = date.day

   conn = mariadb.connect(**config)
   cur = conn.cursor()

   query = "select \
                a.airline, \
                t.carrier airline_code, \
                t.origin, \
                t.dest, \
                t.price, \
                f.dep_time, \
                f.arr_time, \
                fh.avg_delay, \
                (select avg(arr_time - dep_time) from travel_history.flights \
                where month = ? and day = ? and origin = ? and dest = ? and carrier = t.carrier and year >= 2014) avg_duration, \
                fh.delayed_pct, \
                fh.cancelled_pct \
            from \
                travel.tickets t, \
                (select * from travel.flights where year = ? and month = ? and day = ?) f, \
                (select  \
                    a.avg_delay, \
                    round(100 * (a.`delayed` / a.volume), 2) delayed_pct, \
                    round(100 * (a.cancelled / a.volume), 2) cancelled_pct, \
                    a.carrier \
                from \
                    (select \
                        count(*) volume, \
                        sum(case when dep_delay > 0 then 1 else 0 end) `delayed`, \
                        sum(cancelled) cancelled, \
                        avg(dep_delay) avg_delay, \
                        carrier \
                    from  \
                        travel_history.flights \
                    where \
                        year >= 2014 and \
                        month = ? and day = ? and origin = ? and dest = ? group by carrier) a) fh, \
                travel.airlines a  \
            where \
                t.carrier = f.carrier and \
                t.fl_date = f.fl_date and \
                t.fl_num = f.fl_num and \
                t.carrier = fh.carrier and \
                f.carrier = a.iata_code and \
                t.fl_date = ? and \
                t.origin = ? and \
                t.dest = ?"

   cur.execute(query,[month,day,origin,dest,year,month,day,month,day,origin,dest,date,origin,dest])
   row_headers=[x[0] for x in cur.description] 
   rv = cur.fetchall()

   json_data=[]
   for result in rv:
        json_data.append(dict(zip(row_headers,result)))

   if len(json_data) > 0:
       json_data = analyzeResults(json_data)

   return json.dumps(json_data), 200, {'ContentType':'application/json'} 

def analyzeResults(json_data):
   price_sum = 0

   for item in json_data:
        price = item['price']
        price_sum += price

   average_price = price_sum / len(json_data)

   for item in json_data:
       price_score = round(decimal.Decimal(3.5) * (average_price / item['price']), 1)
       delay_score = round(decimal.Decimal(5) * ((100 - item['delayed_pct'])/100), 1)
       cancel_score = round(decimal.Decimal(5) * ((100 - item['cancelled_pct'])/100), 1)
       overall_score = round((price_score + delay_score + cancel_score) / 3, 1)
       assessment = {
           'overall_score': overall_score,
           'price_score': price_score,
           'delay_score': delay_score,
           'delay_percentage': item['delayed_pct'],
           'cancel_score': cancel_score,
           'cancel_percentage': item['cancelled_pct']
       }
       item['assessment'] = assessment

   return json_data


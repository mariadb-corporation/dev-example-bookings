import sys
import simplejson as json
import datetime
import decimal
import mariadb
import os
import flask
from flask import request
from flask import Blueprint
from dotenv import load_dotenv

load_dotenv()

trips = Blueprint('trips', __name__)

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

@trips.route('/api/trips', methods=['GET'])
def index():

   conn = mariadb.connect(**config)
   cur = conn.cursor()

   query = "select \
                t.fl_num, \
                a.airline, \
                t.carrier airline_code, \
                t.fl_date, \
                t.origin, \
                t.dest, \
                f.dep_time, \
                f.arr_time, \
                fh.delayed_pct, \
                fh.avg_delay \
            from \
                travel.trips tr inner join  \
                travel.tickets t on tr.ticket_id = t.id inner join \
                travel.airlines a on t.carrier = a.iata_code, \
                (select * from travel.flights where year >= 2020) f, \
                (select  \
                    a.avg_delay, \
                    round(100 * (a.`delayed` / a.volume), 2) delayed_pct, \
                    round(100 * (a.cancelled / a.volume), 2) cancelled_pct, \
                    a.carrier, \
                    a.day, \
                    a.month \
                from  \
                    (select  \
                        count(*) volume, \
                        sum(case when dep_delay > 0 then 1 else 0 end) `delayed`, \
                        sum(cancelled) cancelled, \
                        avg(dep_delay) avg_delay, \
                        carrier, \
                        month, \
                        day \
                    from  \
                        travel_history.flights \
                    where \
                        year >= 2014 and \
                        month in (select month(fl_date) from travel.trips tr inner join travel.tickets t on tr.ticket_id = t.id) and \
                        day in (select day(fl_date) from travel.trips tr inner join travel.tickets t on tr.ticket_id = t.id) \
                    group by  \
                        day, \
                        month, \
                        carrier) a) fh \
            where \
                t.carrier = f.carrier and \
                t.fl_date = f.fl_date and \
                t.fl_num = f.fl_num and \
                t.carrier = fh.carrier and \
                fh.month = month(t.fl_date) and \
                fh.day = day(t.fl_date)"

   cur.execute(query)
   row_headers=[x[0] for x in cur.description] 
   rv = cur.fetchall()

   json_data=[]
   for result in rv:
        json_data.append(dict(zip(row_headers,result)))

   if len(json_data) > 0:
       json_data = analyzeResults(json_data)

   return json.dumps(json_data, default=converter), 200, {'ContentType':'application/json'} 

def analyzeResults(json_data):
   #TODO: Replace placeholder with (location based) weather API results
   for item in json_data:
       precip_probability = .2
       wind_speed = 10

       weather_score = 5 - 5 * (precip_probability + (wind_speed/100))
       historical_score = round(5 * ((100 - item['delayed_pct'])/100), 1)
       overall_score = round((decimal.Decimal(weather_score) + decimal.Decimal(historical_score)) / 2, 1)
       weather_delay_multiplier = round((precip_probability + (wind_speed/100)) * 5, 3)
       projected_delay = round(decimal.Decimal(weather_delay_multiplier) * item['avg_delay'], 0)

       assessment = {
           'overall_score': overall_score,
           'historical_score': historical_score,
           'historical_delay_percentage': item['delayed_pct'],
           'weather_score': weather_score,
           'weather_delay_multiplier': weather_delay_multiplier,
           'projected_delay': projected_delay
       }

       item['assessment'] = assessment

       forecast = {
           'description': "Clear", 
           'icon': "clear-day",
           'temp_low': "55°F",
           'temp_high': "55°F",
           'precip_probability': precip_probability,
           'wind_speed': wind_speed
       }

       item['forecast'] = forecast

   return json_data


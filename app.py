from flask import Flask, request, jsonify
app = Flask(__name__)
import os
import requests
import json
from database import city_in_da_base, get_city_from_base, write_city_to_base
from env import APPID

@app.route('/')
def index():
    return 'use /weather?city=city_name'

@app.route("/weather", methods = ['GET'])
def get_weather():
    if request.method == 'GET':
        city = request.args.get('city')
        return weather(city)

def weather(city):
    if city_in_da_base(city):
        ans = get_city_from_base(city)
    else:
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={APPID}'
        resp = requests.get(api_url)
        resp_text = json.loads(resp.text)
        ans = {}
        try:
            ans["city"] = resp_text["name"]
            ans["temp"] = resp_text["main"]["temp"]
            ans["pressure"] = round(resp_text["main"]["pressure"]/1.3332239, 2)
            ans["wind"] = resp_text["wind"]["speed"]
            write_city_to_base(ans)
        except:
            ans = resp_text
    return jsonify(ans)
    

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
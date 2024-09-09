# app.py
from flask import Flask, render_template, jsonify, request
import speedtest
import requests
import threading

app = Flask(__name__)

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_ip_information(ip):
    response = requests.get(f'http://ip-api.com/json/{ip}').json()
    return {
        "ip": response.get("query"),
        "country": response.get("country"),
        "countryCode": response.get("countryCode"),
        "city": response.get("city"),
        "region": response.get("regionName")
    }

def perform_speed_test(test_type):
    speed = speedtest.Speedtest()
    speed.get_best_server()
    
    if test_type == "download" or test_type == "both":
        download_speed = round(speed.download() / 1_000_000, 2)
    else:
        download_speed = None
    
    if test_type == "upload" or test_type == "both":
        upload_speed = round(speed.upload() / 1_000_000, 2)
    else:
        upload_speed = None
    
    ping = round(speed.results.ping, 2)
    
    return {
        "download": download_speed,
        "upload": upload_speed,
        "ping": ping
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speed_test', methods=['POST'])
def speed_test():
    test_type = request.json['type']
    results = perform_speed_test(test_type)
    return jsonify(results)

@app.route('/ip_info', methods=['GET'])
def ip_info():
    ip = get_ip()
    info = get_ip_information(ip)
    return jsonify(info)

@app.route('/external_ip_info', methods=['POST'])
def external_ip_info():
    ip = request.json['ip']
    info = get_ip_information(ip)
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True)
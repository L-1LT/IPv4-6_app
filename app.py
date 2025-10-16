from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def get_ip_info(ip: str):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"https://ipapi.co/{ip}/json/", headers=headers, timeout=6)
        data = resp.json()

        return {
            "IP Address": data.get("ip"),
            "City": data.get("city"),
            "Region": data.get("region"),
            "Country": f"{data.get('country_name')} ({data.get('country')})",
            "Postal Code": data.get("postal"),
            "European Union": data.get("in_eu"),
            "Latitude / Longitude": f"{data.get('latitude')}, {data.get('longitude')}",
            "Time Zone": data.get("timezone"),
            "Calling Code": data.get("country_calling_code"),
            "Currency": data.get("currency"),
            "Languages": data.get("languages"),
            "ASN": data.get("asn"),
            "Organization": data.get("org")
        }

    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info')
def get_info():
    ip = request.args.get('ip', '')
    if not ip:
        ip = requests.get("https://api.ipify.org").text
    data = get_ip_info(ip)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)


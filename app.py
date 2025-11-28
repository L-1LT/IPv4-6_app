from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def get_ip_info(ip: str):
    try:
        # 💡 Example Feature 1: Simple IP Validation
        # In a real app, you'd use a regex library, but for simplicity:
        if not ip or not any(char.isdigit() for char in ip):
             raise ValueError("Invalid IP address format.")
             
        headers = {"User-Agent": "Mozilla/5.0"}
        # Note: In a real environment, the API call should be mocked for testing
        resp = requests.get(f"https://ipapi.co/{ip}/json/", headers=headers, timeout=6)
        data = resp.json()

        # Check for API-side error response
        if data.get("error"):
            return {"error": data.get("reason", "API lookup failed.")}

        return {
            "IP Address": data.get("ip"),
            "City": data.get("city"),
            "Region": data.get("region"),
            "Country": f"{data.get('country_name')} ({data.get('country')})",
            "Organization": data.get("org")
        }

    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": f"An external error occurred: {str(e)}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info')
def get_info():
    ip = request.args.get('ip', '')
    if not ip:
        # ⚠️ This external call makes tests slower, but reflects the real logic
        ip = requests.get("https://api.ipify.org").text
    
    data = get_ip_info(ip)
    
    # 💡 Example Feature 2: Return appropriate HTTP status code
    status_code = 400 if 'error' in data else 200
    
    return jsonify(data), status_code

if __name__ == '__main__':
    # Set threaded=True for potential rate limiting testing, though complex for simple Flask
    app.run(debug=True)

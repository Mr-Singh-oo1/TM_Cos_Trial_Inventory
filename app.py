from flask import Flask, request, Response, render_template
import requests
import warnings
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from waitress import serve

# Suppress SSL warnings (safe for public endpoints like Google Apps Script)
warnings.simplefilter('ignore', InsecureRequestWarning)

app = Flask(__name__, template_folder='templates')

# Inventory Google Apps Script endpoint
INVENTORY_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyZhQRHpyJdp3DUSnsNZE-jD0wkS69-hsj0AH8pUzWt_qQFLuKGyMFGYXhJfFMmOefq_g/exec"

# Selling form Google Apps Script endpoint
SALES_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxs5M0ztA-c5AXuNBIQI9BXGXSEEBnCpKqowE_VdrjWF0aViHvQoDNXuos4tw_o1vkC/exec"

# ✅ Serve your frontend form
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')  # index.html must be in /templates

# ✅ Proxy route for inventory form (JSON-only)
@app.route('/submit-inventory', methods=['POST'])
def proxy_inventory():
    try:
        payload = request.get_json(force=True)
        response = requests.post(
            INVENTORY_SCRIPT_URL,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        return Response(
            response.content,
            status=response.status_code,
            content_type='text/plain'
        )
    except Exception as e:
        return Response(f"❌ Inventory Proxy Error: {str(e)}", status=500)

# ✅ Proxy route for selling form (JSON-wrapped)
@app.route('/submit-sale', methods=['POST'])
def proxy_sale():
    try:
        payload = request.get_json(force=True)
        response = requests.post(
            SALES_SCRIPT_URL,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

        try:
            parsed = response.json()
        except ValueError:
            parsed = {"message": response.text}

        wrapped = {
            "ok": True,
            "items": [parsed] if isinstance(parsed, dict) else parsed
        }

        return Response(
            json.dumps(wrapped),
            status=response.status_code,
            content_type='application/json'
        )
    except Exception as e:
        return Response(f"❌ Sales Proxy Error: {str(e)}", status=500)

# ✅ Use Waitress for production
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)



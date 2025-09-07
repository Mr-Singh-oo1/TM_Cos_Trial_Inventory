from flask import Flask, request, Response
import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from waitress import serve

# Suppress SSL warnings (safe for public endpoints like Google Apps Script)
warnings.simplefilter('ignore', InsecureRequestWarning)

app = Flask(__name__)

# Replace with your actual Google Apps Script endpoint
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyZhQRHpyJdp3DUSnsNZE-jD0wkS69-hsj0AH8pUzWt_qQFLuKGyMFGYXhJfFMmOefq_g/exec"

@app.route('/submit-inventory', methods=['POST'])
def proxy_to_google_script():
    try:
        # Forward form fields and files to Google Apps Script
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            data=request.form,
            files=request.files
        )

        # Return the response from Google Apps Script to the frontend
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'text/plain')
        )

    except Exception as e:
        return Response(f"❌ Proxy Error: {str(e)}", status=500)

# Use Waitress to serve the app in production
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)

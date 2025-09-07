from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Replace with your actual Apps Script endpoint
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyZhQRHpyJdp3DUSnsNZE-jD0wkS69-hsj0AH8pUzWt_qQFLuKGyMFGYXhJfFMmOefq_g/exec"

@app.route('/submit-inventory', methods=['POST'])
def proxy_to_google_script():
    try:
        # Forward the form data (including image) to Apps Script
        res = requests.post(GOOGLE_SCRIPT_URL, files=request.files, data=request.form)
        return Response(res.content, status=res.status_code, content_type=res.headers.get('Content-Type'))
    except Exception as e:
        return Response(f"❌ Proxy Error: {str(e)}", status=500)

if __name__ == '__main__':
    app.run(debug=True)
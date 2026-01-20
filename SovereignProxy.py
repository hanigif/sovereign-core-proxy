import os
import time
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# إعدادات الهوية السيادية
SERVER_LOCATION = "Sweden/Stockholm"
# الرابط الذي يستقبل التنبيهات في لوحة تحكم إمبراطوريتك
EMPIRE_RECEIVER_URL = "https://my-empire.onrender.com/receive-intelligence"

def scrub_data(raw_data):
    """تطهير البيانات قبل خروجها من الحدود"""
    clean_data = raw_data.copy()
    clean_data['ip_address'] = "0.0.0.0" # حماية الخصوصية بموجب GDPR
    clean_data['sovereign_audit_trail'] = f"{SERVER_LOCATION}-ACTIVE"
    return clean_data

@app.route('/')
def health_check():
    return f"🛡️ Sovereign Core Proxy is LIVE in {SERVER_LOCATION}", 200

@app.route('/sovereign-gate', methods=['POST', 'OPTIONS'])
def gate():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        return response

    try:
        incoming_data = request.json
        if not incoming_data:
            return jsonify({"status": "Empty Data"}), 400
            
        # 1. تطهير البيانات
        processed_data = scrub_data(incoming_data)
        
        # 2. إرسال تنبيه فوري للوحة التحكم (العقل المدبر)
        try:
            # نرسل اسم المصدر ونوع العملية ليتم عرضها في الجدول
            requests.post(EMPIRE_RECEIVER_URL, json={
                "source": "Sovereign Official Site",
                "risk_level": "SECURE",
                "status": "INTERCEPTED & SCRUBBED"
            }, timeout=5)
        except Exception as e:
            print(f"Failed to notify dashboard: {e}")
        
        # 3. الرد على الموقع بأن البيانات أصبحت آمنة
        res = jsonify({
            "status": "Secured",
            "node": SERVER_LOCATION,
            "compliance": "NIS2 Compliant"
        })
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res, 200

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

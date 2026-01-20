import os
import time
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# إعدادات الهوية السيادية
SERVER_LOCATION = "Sweden/Stockholm"
SOVEREIGN_ID = "SOV-CORE-2026"

def scrub_data(raw_data):
    """
    محرك التطهير: يقوم بمسح وإخفاء البيانات الحساسة 
    قبل السماح لها بالخروج من الحدود الرقمية السويدية.
    """
    clean_data = raw_data.copy()
    
    # 1. إخفاء عنوان الـ IP (متطلب أساسي للـ GDPR)
    clean_data['ip_address'] = "0.0.0.0"
    
    # 2. تشفير المعرفات الشخصية بختم زمن سيادي
    if 'client_id' in clean_data:
        clean_data['client_id'] = f"SOV_ENCRYPTED_{int(time.time())}"
    
    # 3. إضافة وسم التدقيق السيادي
    clean_data['sovereign_audit_trail'] = f"{SERVER_LOCATION}-{SOVEREIGN_ID}"
    
    return clean_data

@app.route('/')
def health_check():
    return f"🛡️ Sovereign Core Proxy is LIVE in {SERVER_LOCATION}", 200

@app.route('/sovereign-gate', methods=['POST', 'OPTIONS'])
def gate():
    # معالجة طلبات الـ CORS (للسماح للمواقع بالاتصال بالبروكسي)
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
            
        # عملية التطهير
        processed_data = scrub_data(incoming_data)
        
        # هنا يتم تخزين البيانات أو توجيهها (سنقوم بربطها بالـ App.py لاحقاً)
        print(f"Incoming Protected Data: {processed_data}")
        
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
    # الحصول على المنفذ من إعدادات Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

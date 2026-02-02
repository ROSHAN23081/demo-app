from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database import db
import random

app = Flask(__name__)
CORS(app)

# ================== USER REGISTRATION FLOW ==================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    success = db.add_user(
        email=data['email'],
        password=data['password'],
        phone=data['phone'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    if success:
        return jsonify({"status": "success", "message": "User registered! OTP sent."})
    return jsonify({"status": "error", "message": "Email or phone already exists"}), 400

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    phone = data['phone']
    otp = data['otp']
    
    # For demo: any 6-digit OTP works (123456)
    if otp == "123456":
        db.verify_user(phone)
        return jsonify({"status": "success", "message": "Phone verified!"})
    return jsonify({"status": "error", "message": "Invalid OTP"}), 400

# ================== BRAND CAMPAIGN FLOW ==================

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    # Simulated data for demo
    campaigns = [
        {
            "id": 1,
            "name": "Summer Sale 2024",
            "status": "completed",
            "recipients": 12450,
            "delivered": 11892,
            "open_rate": 68,
            "has_safety_mark": True
        },
        {
            "id": 2,
            "name": "Welcome Series",
            "status": "running",
            "recipients": 8230,
            "delivered": 8230,
            "open_rate": 82,
            "has_safety_mark": True
        }
    ]
    return jsonify(campaigns)

@app.route('/api/campaigns', methods=['POST'])
def create_campaign():
    data = request.get_json()
    # Here you would save to database and trigger SMS
    return jsonify({
        "status": "success", 
        "message": "Campaign created with MO Safety Mark!",
        "campaign_id": random.randint(1000, 9999)
    })

# ================== FRAUD DETECTION API ==================

@app.route('/api/verify-message', methods=['POST'])
def verify_message():
    data = request.get_json()
    message = data.get('message', '').lower()
    sender = data.get('sender', '')
    
    # Simple AI fraud detection (rule-based for beginners)
    scam_keywords = ['urgent', 'win', 'prize', 'click here', 'bank account frozen', 
                     'irs', 'package failed', 'verify now', 'limited time']
    
    risk_score = 0
    detected_keywords = []
    
    for keyword in scam_keywords:
        if keyword in message:
            risk_score += 20
            detected_keywords.append(keyword)
    
    # Check if sender is verified brand
    is_verified_brand = sender.startswith('+1') == False  # Simple check
    
    if is_verified_brand and risk_score < 40:
        return jsonify({
            "is_safe": True,
            "safety_mark": True,
            "message": "✓ MO Verified - This message is safe",
            "brand_trust_score": 95
        })
    else:
        return jsonify({
            "is_safe": False,
            "safety_mark": False,
            "message": "⚠ Warning: Potential scam detected",
            "risk_score": risk_score,
            "detected_issues": detected_keywords
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

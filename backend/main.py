from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
# هذا السطر هو الذي يسمح للموقع بأخذ البيانات
CORS(app)

# تحميل البيانات
def load_data():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'data.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"careers": []}

@app.route('/')
def home():
    return "Backend is running correctly!"

@app.route('/api/careers', methods=['GET'])
def get_careers():
    data = load_data()
    careers_list = []
    for career in data.get('careers', []):
        careers_list.append({
            "name": career['name'],
            "prompt_count": len(career.get('prompts_en', []))
        })
    return jsonify({"success": True, "careers": careers_list})

@app.route('/api/careers/<path:career_name>/prompts', methods=['GET'])
def get_prompts(career_name):
    data = load_data()
    # البحث عن المهنة (بدون حساسيه لحالة الأحرف)
    career = next((c for c in data.get('careers', []) if c['name'].lower() == career_name.lower()), None)
    
    if career:
        return jsonify({
            "success": True, 
            "career": career['name'],
            "prompts_ar": career.get('prompts_ar', []),
            "prompts_en": career.get('prompts_en', []),
            "suggested_ai_tools": career.get('suggested_ai_tools', []),
            "prompt_count": len(career.get('prompts_en', []))
        })
    return jsonify({"success": False, "message": "Career not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

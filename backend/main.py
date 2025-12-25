from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

def load_data():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'structured_career_data.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return []

@app.route('/')
def home():
    return "Backend is running!"

@app.route('/api/careers', methods=['GET'])
def get_careers():
    data = load_data()
    careers_list = []
    
    # التعامل مع البيانات سواء كانت قائمة أو قاموس
    careers_data = data.get('careers', []) if isinstance(data, dict) else data

    if not careers_data: 
        return jsonify({"success": False, "careers": []})
        
    for career in careers_data:
        if isinstance(career, dict):
            # 1. قراءة الاسم
            name = career.get('care_name', 'Unknown')
            
            # 2. قراءة عدد الأوامر مباشرة من القائمة الإنجليزية الموجودة في ملفك
            # (حسب السجل الذي أرسلته: prompts_en)
            prompts_en = career.get('prompts_en', [])
            
            careers_list.append({
                "name": name,
                "prompt_count": len(prompts_en)
            })
            
    return jsonify({"success": True, "careers": careers_list})

@app.route('/api/careers/<path:career_name>/prompts', methods=['GET'])
def get_prompts(career_name):
    data = load_data()
    careers_data = data.get('careers', []) if isinstance(data, dict) else data
    
    # البحث عن المهنة
    found_career = None
    for c in careers_data:
        c_name = c.get('care_name', '')
        if c_name.strip().lower() == career_name.strip().lower():
            found_career = c
            break
    
    if found_career:
        # قراءة القوائم مباشرة كما ظهرت في السجل
        prompts_en = found_career.get('prompts_en', [])
        prompts_ar = found_career.get('prompts_ar', [])
        
        return jsonify({
            "success": True, 
            "career": found_career.get('care_name'),
            "prompts_ar": prompts_ar,
            "prompts_en": prompts_en,
            "suggested_ai_tools": found_career.get('suggested_ai_tools', []),
            "prompt_count": len(prompts_en)
        })
        
    return jsonify({"success": False, "message": "Career not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

def load_data():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # استخدام الاسم الصحيح للملف
        file_path = os.path.join(base_dir, 'structured_career_data.json')
        print(f"Loading data from: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: File not found!")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

@app.route('/')
def home():
    return "Backend is running correctly!"

@app.route('/api/careers', methods=['GET'])
def get_careers():
    data = load_data()
    careers_list = []
    
    # التعامل مع البيانات سواء كانت قائمة مباشرة أو داخل مفتاح
    careers_data = data.get('careers', []) if isinstance(data, dict) else data

    if not careers_data:
         return jsonify({"success": False, "message": "No data found", "careers": []})
        
    for career in careers_data:
        if isinstance(career, dict):
            # 1. قراءة الاسم من المفتاح الصحيح "care_name"
            name = career.get('care_name', 'Unknown')
            
            # 2. حساب عدد الأوامر من قائمة "prompts"
            prompts = career.get('prompts', [])
            
            careers_list.append({
                "name": name,
                "prompt_count": len(prompts)
            })
            
    return jsonify({"success": True, "careers": careers_list})

@app.route('/api/careers/<path:career_name>/prompts', methods=['GET'])
def get_prompts(career_name):
    data = load_data()
    careers_data = data.get('careers', []) if isinstance(data, dict) else data
    
    # البحث عن المهنة باستخدام "care_name"
    career = next((c for c in careers_data if isinstance(c, dict) and c.get('care_name', '').lower() == career_name.lower()), None)
    
    if career:
        # استخراج الأوامر من الهيكلة الجديدة
        raw_prompts = career.get('prompts', [])
        
        # تحويل الأوامر لقائمتين (عربي وإنجليزي) لتناسب الواجهة
        prompts_en = []
        prompts_ar = []
        
        for p in raw_prompts:
            text_obj = p.get('text', {})
            if text_obj.get('en'):
                prompts_en.append(text_obj['en'])
            if text_obj.get('ar'):
                prompts_ar.append(text_obj['ar'])

        return jsonify({
            "success": True, 
            "career": career.get('care_name'),
            "prompts_ar": prompts_ar,
            "prompts_en": prompts_en,
            "suggested_ai_tools": career.get('suggested_ai_tools', []),
            "prompt_count": len(prompts_en)
        })
        
    return jsonify({"success": False, "message": "Career not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

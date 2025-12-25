from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

def load_data():
    try:
        # 1. تحديد مكان الكود الحالي بدقة
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 2. البحث عن الملف بالاسم الحقيقي الموجود عندك
        # (لاحظ أننا وضعنا الاسم الطويل هنا)
        file_path = os.path.join(base_dir, 'structured_career_data.json')
        
        print(f"Loading data from: {file_path}") 
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: File not found!")
        return {"careers": []}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"careers": []}

@app.route('/')
def home():
    return "Backend is running correctly!"

@app.route('/api/careers', methods=['GET'])
def get_careers():
    data = load_data()
    careers_list = []
    
    # التعامل بذكاء سواء كان الملف يبدأ بقائمة أو قاموس
    if isinstance(data, dict):
        careers_data = data.get('careers', [])
    else:
        careers_data = data

    if not careers_data:
         return jsonify({"success": False, "message": "No data found", "careers": []})
        
    for career in careers_data:
        if isinstance(career, dict):
            careers_list.append({
                "name": career.get('name', 'Unknown'),
                "prompt_count": len(career.get('prompts_en', []))
            })
            
    return jsonify({"success": True, "careers": careers_list})

@app.route('/api/careers/<path:career_name>/prompts', methods=['GET'])
def get_prompts(career_name):
    data = load_data()
    
    if isinstance(data, dict):
        careers_data = data.get('careers', [])
    else:
        careers_data = data
    
    career = next((c for c in careers_data if isinstance(c, dict) and c.get('name', '').lower() == career_name.lower()), None)
    
    if career:
        return jsonify({
            "success": True, 
            "career": career.get('name'),
            "prompts_ar": career.get('prompts_ar', []),
            "prompts_en": career.get('prompts_en', []),
            "suggested_ai_tools": career.get('suggested_ai_tools', []),
            "prompt_count": len(career.get('prompts_en', []))
        })
    return jsonify({"success": False, "message": "Career not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

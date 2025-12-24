from flask import Blueprint, jsonify
import json
import os

careers_bp = Blueprint('careers', __name__)

def get_json_path():
    # دالة تحديد مسار ملف البيانات بدقة
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(os.path.dirname(current_dir))
    return os.path.join(backend_dir, 'structured_career_data.json')

@careers_bp.route('/careers', methods=['GET'])
def get_careers():
    try:
        data_path = get_json_path()
        if not os.path.exists(data_path):
            return jsonify({'success': False, 'error': 'Data file not found'}), 404

        with open(data_path, 'r', encoding='utf-8') as f:
            careers_data = json.load(f)
        
        careers_list = []
        for career in careers_data:
            careers_list.append({
                'name': career['care_name'],
                'prompt_count': career['num_prompts']
            })
        
        return jsonify({'success': True, 'careers': careers_list})
    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@careers_bp.route('/careers/<career_name>/prompts', methods=['GET'])
def get_career_prompts(career_name):
    try:
        data_path = get_json_path()
        with open(data_path, 'r', encoding='utf-8') as f:
            careers_data = json.load(f)
        
        career_data = next((item for item in careers_data if item["care_name"] == career_name), None)
        
        if not career_data:
            return jsonify({'success': False, 'error': 'Career not found'}), 404

        # قائمة الأدوات مع الروابط
        ai_tools = [
            {"name": "ChatGPT", "url": "https://chat.openai.com"},
            {"name": "Claude", "url": "https://claude.ai"},
            {"name": "Gemini", "url": "https://gemini.google.com"},
            {"name": "Midjourney", "url": "https://www.midjourney.com"},
            {"name": "Jasper", "url": "https://www.jasper.ai"}
        ]
        
        return jsonify({
            'success': True,
            'career': career_data['care_name'],
            'prompt_count': career_data['num_prompts'],
            'prompts_en': career_data.get('prompts_en', []),
            'prompts_ar': career_data.get('prompts_ar', []),
            'suggested_ai_tools': ai_tools
        })
    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
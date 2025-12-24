import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# إضافة المجلد الحالي للمسار لضمان عمل الاستيراد بشكل صحيح
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.routes.careers import careers_bp
except ImportError as e:
    print("Error importing careers_bp. Please check your folder structure.")
    print(f"Details: {e}")
    sys.exit(1)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-123'

# السماح للواجهة الأمامية بالاتصال بالسيرفر
CORS(app)

# تسجيل المسار الخاص بالمهن فقط
app.register_blueprint(careers_bp, url_prefix='/api')

@app.route('/')
def home():
    return "Server is running! You can now request /api/careers"

if __name__ == '__main__':
    print("Starting Flask Server...")
    # تشغيل السيرفر على المنفذ 5000
    app.run(debug=True, port=5000)
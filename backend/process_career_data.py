import pandas as pd
import json
import os

# تحديد المسارات
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'career_data.csv')
json_path = os.path.join(current_dir, 'structured_career_data.json')

print(f"Reading CSV from: {csv_path}")

try:
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip() # تنظيف أسماء الأعمدة

    # ---------------------------------------------------------
    # ⚠️ هام جداً: غير الأسماء هنا لتطابق الموجودة في ملفك CSV
    col_english = 'prom_career'       # اسم عمود الأوامر الإنجليزية
    col_arabic = 'prom_career_ar'     # اسم عمود الأوامر العربية (تأكد من الاسم)
    # ---------------------------------------------------------

    # التأكد من وجود الأعمدة
    if col_english not in df.columns:
        print(f"❌ Error: Column '{col_english}' not found!")
    # هنا نتأكد من وجود العمود العربي، لو غير موجود سنستخدم الإنجليزي مؤقتاً لتجنب الخطأ
    if col_arabic not in df.columns:
        print(f"⚠️ Warning: Column '{col_arabic}' not found. Using English column for both.")
        df[col_arabic] = df[col_english]

    # 1. حساب عدد الأوامر
    career_counts = df.groupby('care_name').size().reset_index(name='num_prompts')

    # 2. تجميع الأوامر الإنجليزية في قائمة
    prompts_en = df.groupby('care_name')[col_english].apply(list).reset_index(name='prompts_en')

    # 3. تجميع الأوامر العربية في قائمة
    prompts_ar = df.groupby('care_name')[col_arabic].apply(list).reset_index(name='prompts_ar')

    # 4. دمج الجداول
    merged_df = pd.merge(career_counts, prompts_en, on='care_name')
    merged_df = pd.merge(merged_df, prompts_ar, on='care_name')

    # 5. الحفظ
    output_data = merged_df.to_dict(orient='records')

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Success! Generated JSON with dual language support.")

except Exception as e:
    print(f"❌ Error: {e}")
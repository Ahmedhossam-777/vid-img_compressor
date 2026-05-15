# 🗜️ Universal File Compressor

Web app لضغط الصور والفيديوهات — مبني بـ Streamlit.

## الملفات
- `app.py` — الكود الرئيسي
- `requirements.txt` — المكتبات
- `Procfile` — أمر التشغيل على Railway
- `nixpacks.toml` — تثبيت ffmpeg على السيرفر

## رفع على Railway

1. ارفع الملفات على GitHub repo جديد
2. روح على https://railway.app وسجل دخول
3. اضغط **New Project → Deploy from GitHub**
4. اختار الـ repo
5. Railway هيعمل كل حاجة تلقائياً ✅
6. بعد الـ deploy اضغط **Settings → Generate Domain**

## تشغيل محلي

pip install -r requirements.txt
streamlit run app.py

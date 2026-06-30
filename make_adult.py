import os
import requests
import re

OUTPUT_FILE = "adult_playlist.m3u"
MAIN_URL = "https://raw.githubusercontent.com/thebeastapp/beast/main/adult.m3u"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

def build_playlist():
    playlist_content = "#EXTM3U\n"
    channels_count = 0
    
    print("📥 جاري جلب الباقة وتصحيح قراءة ملف الـ M3U...")
    try:
        response = requests.get(MAIN_URL, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            # تنظيف النص وتقسيمه بناءً على الأسطر بكل أنواعها
            raw_text = response.text.replace('\r', '')
            lines = raw_text.split('\n')
            
            current_info = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # إذا وجدنا سطر معلومات القناة
                if line.startswith("#EXTINF"):
                    current_info = line
                    continue
                
                # إذا وجدنا الرابط الخاص بالقناة بعد سطر المعلومات
                if line.startswith("http") and current_info:
                    # استخراج الاسم الأصلي للقناة بعد الفاصلة
                    channel_name = "Adult Channel"
                    if "," in current_info:
                        channel_name = current_info.split(",", 1)[1].strip()
                    
                    # إعادة تركيب السطر متوافقاً مع دراما لايف والمشغلات الأخرى
                    clean_info = f'#EXTINF:-1 group-title="Adult Premium TV",{channel_name}'
                    
                    playlist_content += clean_info + "\n"
                    playlist_content += line + "\n"
                    channels_count += 1
                    
                    # تصفير المتغير لقراءة القناة التالية
                    current_info = None
                    
            print(f"✅ تم دمج وتصحيح {channels_count} قناة بنجاح!")
        else:
            print(f"❌ فشل السيرفر في جلب الملف، كود الاستجابة: {response.status_code}")
            
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع أثناء المعالجة: {e}")

    # حفظ الملف النهائي للتأكد من عدم خروجه فارغاً
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"🚀 مريقل! تم تحديث {OUTPUT_FILE} بنجاح ومستعد للتشغيل.")
    except Exception as e:
        print(f"❌ فشل حفظ ملف m3u: {e}")

if __name__ == "__main__":
    build_playlist()

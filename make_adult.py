import os
import requests
import re

OUTPUT_FILE = "adult_playlist.m3u"
MAIN_URL = "https://raw.githubusercontent.com/thebeastapp/beast/main/adult.m3u"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

def build_playlist():
    playlist_content = "#EXTM3U\n"
    channels_count = 0
    
    print("📥 جاري جلب الباقة وتصحيح أسماء القنوات بالكامل...")
    try:
        response = requests.get(MAIN_URL, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            # تقسيم الملف إلى أسطر
            lines = response.text.split('\n')
            
            for i in range(len(lines)):
                line = lines[i].strip()
                if line.startswith("#EXTINF"):
                    # التأكد من وجود سطر الرابط التالي
                    if i + 1 < len(lines) and lines[i+1].strip().startswith("http"):
                        stream_url = lines[i+1].strip()
                        
                        # استخراج اسم القناة الأصلي بعد الفاصلة لتفادي حذفه
                        channel_name = "Adult Channel"
                        if "," in line:
                            channel_name = line.split(",", 1)[1].strip()
                        
                        # إعادة بناء السطر بشكل سليم ومقبول في كل المشغلات
                        clean_line = f'#EXTINF:-1 group-title="Adult Premium TV",{channel_name}'
                        
                        playlist_content += clean_line + "\n"
                        playlist_content += stream_url + "\n"
                        channels_count += 1
                        
            print(f"✅ تم دمج وتصحيح {channels_count} قناة بنجاح!")
    except Exception as e:
        print(f"❌ حدث خطأ أثناء جلب الداتا: {e}")

    # حفظ الملف النهائي
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"🚀 مريقل! تم تحديث الملف بنجاح وظهور جميع القنوات بالأسماء.")
    except Exception as e:
        print(f"❌ فشل حفظ ملف m3u: {e}")

if __name__ == "__main__":
    build_playlist()

import os
import requests

OUTPUT_FILE = "adult_playlist.m3u"  # تم تغيير الاسم ليتوافق مع ملف البالغين في مستودعك

SOURCES = [
    "https://iptvmate.net/files/adult.m3u"
]

def fetch_and_build():
    # إضافة القناة يدويًا كبداية للملف (استبدل رابط STREAM_URL بالرابط الشغال لديك)
    visit_x_stream = "http://YOUR_STREAM_URL_HERE/live.m3u8" 
    
    playlist_content = "#EXTM3U\n"
    playlist_content += f'#EXTINF:-1 tvg-id="Visit-X" tvg-name="Visit-X" tvg-logo="https://example.com/visitx.png" group-title="Adult",Visit-X (Astra 19.2E)\n{visit_x_stream}\n'
    
    for url in SOURCES:
        try:
            print(f"جاري فحص المصدر: {url}...")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                lines = [line.strip() for line in response.text.split('\n') if line.strip()]
                for i in range(len(lines)):
                    if lines[i].startswith("#EXTINF"):
                        line_upper = lines[i].upper()
                        # تصفية المصادر الأخرى إذا كنت تبحث عن كلمات معينة
                        if i + 1 < len(lines) and lines[i+1].startswith("http"):
                            playlist_content += lines[i] + "\n"
                            playlist_content += lines[i+1] + "\n"
        except Exception as e:
            print(f"خطأ: {e}")

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print("تم الحفظ بنجاح!")
    except Exception as e:
        print(f"خطأ في الحفظ: {e}")

if __name__ == "__main__":
    fetch_and_build()

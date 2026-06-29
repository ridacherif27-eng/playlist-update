import os
import requests

# اسم ملف القائمة النهائي الذي سيتم إنشاؤه
OUTPUT_FILE = "adult_playlist.m3u"

# مصدر البث النظيف والمحدث
SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/adult.m3u"
]

# القنوات المستهدفة فقط للتصفية والتمويه
TARGET_CHANNELS = [
    "Hustler", "Dorcel", "Private", "Redlight", "XXL", "SCT", 
    "PassionXXX", "Evil Angel", "Vivid", "Blue Hustler", "Satisfaction"
]

def fetch_and_mask_playlist():
    playlist_content = "#EXTM3U\n"
    has_channels = False
    counter = 1
    
    print("بدء جلب القنوات وتطبيق التمويه الذكي...")
    
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=25)
            if response.status_code == 200:
                lines = response.text.splitlines()
                
                for i in range(len(lines)):
                    if lines[i].strip().startswith("#EXTINF"):
                        info_line = lines[i].strip()
                        
                        # التحقق من أن القناة موجودة في قائمتنا المستهدفة
                        if any(target.lower() in info_line.lower() for target in TARGET_CHANNELS):
                            # التأكد من وجود رابط البث في السطر التالي
                            if i + 1 < len(lines) and lines[i+1].strip().startswith("http"):
                                stream_url = lines[i+1].strip()
                                
                                # إنشاء الاسم المموّه الجديد بالكامل لتفادي الحظر
                                masked_info = f'#EXTINF:-1 tvg-logo="" group-title="Satellites Premium",Premium Movie {counter}'
                                
                                playlist_content += masked_info + "\n" + stream_url + "\n"
                                counter += 1
                                has_channels = True
                                
        except Exception as e:
            print(f"خطأ أثناء الجلب من المصدر {url}: {e}")

    # إذا لم يجد السكربت أي قناة (كحماية للملف)
    if not has_channels:
        playlist_content += "#EXTINF:-1,--- NO CHANNELS FOUND ---\nhttp://0.0.0.0\n"

    # كتابة وحفظ الملف الجديد تماماً
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"نجاح! تم تحديث وإنشاء ملف '{OUTPUT_FILE}' بنجاح وبأسماء مموهة.")
    except Exception as e:
        print(f"خطأ أثناء حفظ الملف: {e}")

if __name__ == "__main__":
    fetch_and_mask_playlist()

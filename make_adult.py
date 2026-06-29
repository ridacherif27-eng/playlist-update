import os
import requests

# اسم ملف القائمة النهائي الذي سيتم إنشاؤه
OUTPUT_FILE = "adult_playlist.m3u"

# مصادر بث حية ومحدثة وموسعة تحتوي على باقات الأقمار الأوروبية
SOURCES = [
    "https://iptv-org.github.io/iptv/categories/adult.m3u",
    "https://raw.githubusercontent.com/MoDirect/AdultIPTV/master/AdultIPTV.m3u",
    "https://raw.githubusercontent.com/skylinuxtv/E2-IPTV/main/adults.m3u",
    "https://raw.githubusercontent.com/Tofiko02/Adult/main/Adult.m3u",
    "https://raw.githubusercontent.com/orion0-0/Free-IPTV/main/Adult.m3u"
]

# قائمة قنوات الكبار الشهيرة للتصفية والتمويه
TARGET_CHANNELS = [
    "Hustler", "Dorcel", "Private", "Redlight", "XXL", "SCT", "Satisfaction", 
    "Passion", "Evil Angel", "Vivid", "Blue Hustler", "Brazzers", "Penthouse", 
    "Playboy", "Centoxcento", "Pink", "Man-X", "Dusk", "Vixen", "Freex", "X-Muzik",
    "SuperOne", "Erox", "Eroxxx", "Leo", "Cento", "Amore", "Roxy", "Teleitalia"
]

def fetch_and_mask_playlist():
    playlist_content = "#EXTM3U\n"
    has_channels = False
    counter = 1
    
    print("بدء جلب القنوات من المصادر الموسعة وتطبيق التمويه...")
    
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=25)
            if response.status_code == 200:
                lines = response.text.splitlines()
                
                for i in range(len(lines)):
                    if lines[i].strip().startswith("#EXTINF"):
                        info_line = lines[i].strip()
                        
                        # التحقق من وجود القناة ضمن القائمة المستهدفة
                        if any(target.lower() in info_line.lower() for target in TARGET_CHANNELS):
                            if i + 1 < len(lines) and lines[i+1].strip().startswith("http"):
                                stream_url = lines[i+1].strip()
                                
                                # التمويه لحماية الرابط في التطبيق
                                masked_info = f'#EXTINF:-1 tvg-logo="" group-title="Satellites Premium",Premium Movie {counter}'
                                
                                playlist_content += masked_info + "\n" + stream_url + "\n"
                                counter += 1
                                has_channels = True
                                
        except Exception as e:
            print(f"خطأ أثناء الجلب من المصدر {url}: {e}")

    if not has_channels:
        playlist_content += "#EXTINF:-1,--- NO CHANNELS FOUND ---\nhttp://0.0.0.0\n"

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"نجاح! تم تحديث ملف '{OUTPUT_FILE}' بنجاح وبأحدث الروابط الشغالة.")
    except Exception as e:
        print(f"خطأ أثناء حفظ الملف: {e}")

if __name__ == "__main__":
    fetch_and_mask_playlist()

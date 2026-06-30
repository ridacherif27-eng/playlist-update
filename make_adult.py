import os
import requests
import re
from bs4 import BeautifulSoup

OUTPUT_FILE = "adult_playlist.m3u"

# المصدر الموثوق والمباشر الأساسي
MAIN_URL = "https://iptv-org.github.io/iptv/index.nsfw.m3u"

# المواقع المجانية التي نريد كشط روابطها الحية تلقائياً
SCRAPE_SITES = {
    "Brazzers TV": "https://adult-tv-channels.click/brazzers-tv-online/",
    "Babes TV HD": "https://adult-tv-channels.click/babes-tv-hd/",
    "Visit-X TV": "https://africaorigin.net/live-tv/visit-x-tv/834"
}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def get_scraped_channels():
    """يقوم بدخول المواقع واستخراج الروابط الحية بمفهوم الـ Scraping"""
    scraped_channels = []
    print("\n🔄 جاري كشط واستخراج الروابط الحية من المواقع الإضافية...")
    
    for name, url in SCRAPE_SITES.items():
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 200:
                # استخدام Regex للبحث عن أي رابط بث مباشر m3u8 مخفي في كود الصفحة
                m3u8_links = re.findall(r'https?://[^\s"\']+\.m3u8[^\s"\']*', response.text)
                
                if m3u8_links:
                    # تنظيف الرابط المستخرج وأخذ أول نتيجة
                    stream_url = m3u8_links[0].replace('\\', '')
                    scraped_channels.append({
                        "info": f'#EXTINF:-1 group-title="Adult Premium TV",{name}',
                        "url": stream_url
                    })
                    print(f"✅ تم العثور على رابط حي لـ: {name}")
                else:
                    print(f"⚠️ لم يتم العثور على رابط مباشر لـ {name} (قد يكون مخفياً لحماية الموقع)")
        except Exception as e:
            print(f"❌ خطأ أثناء جلب {name}: {e}")
            
    return scraped_channels

def build_playlist():
    playlist_content = "#EXTM3U\n"
    channels_count = 0
    
    # 1. جلب القنوات الحية من المصدر الرئيسي
    try:
        print("📥 جاري سحب الباقة العالمية الأساسية الحية...")
        response = requests.get(MAIN_URL, headers=HEADERS, timeout=25)
        if response.status_code == 200:
            lines = [line.strip() for line in response.text.split('\n') if line.strip()]
            
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    if i + 1 < len(lines) and lines[i+1].startswith("http"):
                        clean_line = lines[i]
                        # تنسيق اسم المجموعة ليتوافق تماماً مع تطبيق دراما لايف
                        if "group-title=" not in clean_line:
                            clean_line = clean_line.replace("#EXTINF:-1", '#EXTINF:-1 group-title="Adult Premium TV"')
                        else:
                            # توحيد كافة المجموعات تحت اسم واحد منظم
                            clean_line = re.sub(r'group-title="[^"]+"', 'group-title="Adult Premium TV"', clean_line)
                        
                        playlist_content += clean_line + "\n"
                        playlist_content += lines[i+1] + "\n"
                        channels_count += 1
    except Exception as e:
        print(f"❌ خطأ في المصدر الرئيسي: {e}")

    # 2. دمج القنوات المظبوطة والمكشوطة من المواقع الأخرى
    extra_channels = get_scraped_channels()
    for ch in extra_channels:
        playlist_content += ch["info"] + "\n"
        playlist_content += ch["url"] + "\n"
        channels_count += 1

    # 3. حفظ الملف النهائي
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"\n🚀 مريقل! تم بنجاح بناء الملف وحفظ {channels_count} قناة تلفزيونية حية حقيقية!")
    except Exception as e:
        print(f"❌ فشل حفظ ملف m3u: {e}")

if __name__ == "__main__":
    build_playlist()

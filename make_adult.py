import os
import requests
import re
from bs4 import BeautifulSoup

OUTPUT_FILE = "adult_playlist.m3u"

# تم تحديث الرابط إلى رابط البث المباشر المجمع والأكثر استقراراً
MAIN_URL = "https://iptv-org.github.io/iptv/categories/nsfw.m3u"

# المواقع الـ 3 التي قمنا بكشطها بنجاح
SCRAPE_SITES = {
    "Brazzers TV": "https://adult-tv-channels.click/brazzers-tv-online/",
    "Babes TV HD": "https://adult-tv-channels.click/babes-tv-hd/",
    "Visit-X TV": "https://africaorigin.net/live-tv/visit-x-tv/834"
}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def get_scraped_channels():
    scraped_channels = []
    print("\n🔄 جاري كشط واستخراج الروابط الحية من المواقع الـ 3...")
    
    for name, url in SCRAPE_SITES.items():
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 200:
                m3u8_links = re.findall(r'https?://[^\s"\']+\.m3u8[^\s"\']*', response.text)
                if m3u8_links:
                    stream_url = m3u8_links[0].replace('\\', '')
                    scraped_channels.append({
                        "info": f'#EXTINF:-1 group-title="Adult Premium TV",{name}',
                        "url": stream_url
                    })
                    print(f"✅ تم العثور على رابط حي لـ: {name}")
        except Exception as e:
            print(f"❌ خطأ أثناء جلب {name}: {e}")
            
    return scraped_channels

def build_playlist():
    playlist_content = "#EXTM3U\n"
    channels_count = 0
    
    # 1. دمج القنوات الـ 3 المكشوطة أولاً لضمان وجودها دائماً
    extra_channels = get_scraped_channels()
    for ch in extra_channels:
        playlist_content += ch["info"] + "\n"
        playlist_content += ch["url"] + "\n"
        channels_count += 1

    # 2. جلب القنوات الحية من المصدر العالمي الجديد
    try:
        print("\n📥 جاري سحب الباقة العالمية الإضافية...")
        response = requests.get(MAIN_URL, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            lines = [line.strip() for line in response.text.split('\n') if line.strip()]
            
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    if i + 1 < len(lines) and lines[i+1].startswith("http"):
                        clean_line = lines[i]
                        # توحيد اسم المجموعة لتظهر مدمجة في دراما لايف
                        if "group-title=" not in clean_line:
                            clean_line = clean_line.replace("#EXTINF:-1", '#EXTINF:-1 group-title="Adult Premium TV"')
                        else:
                            clean_line = re.sub(r'group-title="[^"]+"', 'group-title="Adult Premium TV"', clean_line)
                        
                        playlist_content += clean_line + "\n"
                        playlist_content += lines[i+1] + "\n"
                        channels_count += 1
            print(f"✅ تم جلب الباقة العالمية بنجاح!")
        else:
            print(f"⚠️ المصدر العالمي استجاب برمز خطأ: {response.status_code} (سيتم الاعتماد على القنوات الـ 3 حالياً)")
    except Exception as e:
        print(f"❌ فشل الاتصال بالمصدر العالمي: {e} (تم الاحتفاظ بالقنوات الـ 3)")

    # 3. حفظ الملف النهائي
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"\n🚀 مريقل! تم تحديث الملف وحفظ {channels_count} قناة كاملة!")
    except Exception as e:
        print(f"❌ فشل حفظ ملف m3u: {e}")

if __name__ == "__main__":
    build_playlist()

import os
import requests
import re
from bs4 import BeautifulSoup

OUTPUT_FILE = "adult_playlist.m3u"
MAIN_URL = "https://raw.githubusercontent.com/thebeastapp/beast/main/adult.m3u"

# التركيز على روابط باقة Brazzers بمختلف السيرفرات لضمان اشتغالها
BRAZZERS_SITES = {
    "Brazzers TV Digital": "https://adult-tv-channels.click/brazzers-tv-online/",
    "Brazzers TV Europe HD": "https://adult-tv-channels.click/brazzers-tv-europe-online/",
    "Brazzers TV Player 1": "https://adult-tv-channels.click/babes-tv-hd/", # سيرفر احتياطي يبث نفس الباقة
    "Brazzers Premium Live": "https://adult-tv-channels.click/hustler-tv-online/"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

def get_brazzers_channels():
    scraped = []
    print("\n🔄 جاري محاولة كشط باقة Brazzers وتأمين الروابط الحية...")
    
    for name, url in BRAZZERS_SITES.items():
        try:
            # استخدام Session لتجاوز بعض قيود الحماية
            session = requests.Session()
            response = session.get(url, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                # البحث عن روابط m3u8 بكل الصيغ الممكنة
                m3u8_links = re.findall(r'https?://[^\s"\']+\.m3u8[^\s"\']*', response.text)
                if m3u8_links:
                    stream_url = m3u8_links[0].replace('\\', '')
                    scraped.append({
                        "info": f'#EXTINF:-1 group-title="Brazzers Premium Network",{name}',
                        "url": stream_url
                    })
                    print(f"✅ تم بنجاح جلب رابط حي لـ: {name}")
        except Exception as e:
            print(f"❌ تعذر الاتصال بـ {name}: {e}")
            
    return scraped

def build_playlist():
    playlist_content = "#EXTM3U\n"
    channels_count = 0
    
    # 1. تثبيت قنوات Brazzers المستخرجة في أول الملف لتظهر فوراً
    brazzers_channels = get_brazzers_channels()
    for ch in brazzers_channels:
        playlist_content += ch["info"] + "\n"
        playlist_content += ch["url"] + "\n"
        channels_count += 1

    # 2. جلب الباقة الاحتياطية العامة لضمان عدم بقاء الملف فارغاً
    try:
        print("\n📥 جاري دمج الباقة الاحتياطية لزيادة عدد القنوات...")
        response = requests.get(MAIN_URL, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            lines = [line.strip() for line in response.text.split('\n') if line.strip()]
            
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    if i + 1 < len(lines) and lines[i+1].startswith("http"):
                        clean_line = lines[i]
                        # توحيد اسم المجموعة للباقة الاحتياطية
                        if "group-title=" not in clean_line:
                            clean_line = clean_line.replace("#EXTINF:-1", '#EXTINF:-1 group-title="Adult Premium TV"')
                        else:
                            clean_line = re.sub(r'group-title="[^"]+"', 'group-title="Adult Premium TV"', clean_line)
                        
                        playlist_content += clean_line + "\n"
                        playlist_content += lines[i+1] + "\n"
                        channels_count += 1
            print(f"✅ تم دمج الباقة الاحتياطية بنجاح!")
    except Exception as e:
        print(f"❌ فشل الاتصال بالباقة الاحتياطية: {e}")

    # 3. حفظ الملف النهائي
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"\n🚀 مريقل! تم تحديث الملف وحفظ {channels_count} قناة مع التركيز على Brazzers.")
    except Exception as e:
        print(f"❌ فشل حفظ ملف m3u: {e}")

if __name__ == "__main__":
    build_playlist()

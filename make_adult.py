import os
import requests
import re
from bs4 import BeautifulSoup

OUTPUT_FILE = "adult_playlist.m3u"
# الباقة الاحتياطية العامة لملء القائمة بالكامل
MAIN_URL = "https://raw.githubusercontent.com/thebeastapp/beast/main/adult.m3u"
# الصفحة الرئيسية للموقع التي تحتوي على الداتا الكاملة لجميع القنوات
BASE_SITE = "https://adult-tv-channels.click/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Referer": "https://adult-tv-channels.click/"
}

def get_all_site_channels():
    scraped_channels = []
    print("🔄 جاري الاتصال بالسيرفر الرئيسي لكشط جميع القنوات دفعة واحدة...")
    
    try:
        session = requests.Session()
        response = session.get(BASE_SITE, headers=HEADERS, timeout=20)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # البحث عن جميع عناصر القنوات في الصفحة الرئيسية
            # الموقع يعتمد على مربعات (cards/articles) تحتوي على روابط الصفحات والأسماء
            channel_elements = soup.find_all('a', href=True)
            
            # فلترة الروابط الفرعية للقنوات لتجنب التكرار وحظر السيرفر
            valid_urls = set()
            for elem in channel_elements:
                href = elem['href']
                title = elem.get_text().strip()
                if "/online/" in href or "-tv" in href:
                    if href.startswith("https://adult-tv-channels.click/"):
                        name = title if title else href.split('/')[-2].replace('-', ' ').title()
                        # إزالة الكلمات الزائدة لترتيب الاسم في دراما لايف
                        name = name.replace("Online", "").replace("Free", "").strip()
                        if name and len(name) > 3:
                            valid_urls.add((name, href))
            
            print(f"📡 تم العثور على {len(valid_urls)} قناة مستهدفة. جاري استخراج روابط الـ m3u8 الحية...")
            
            # الدخول بكفاءة واستخراج الروابط
            for name, ch_url in list(valid_urls)[:45]: # جلب كافة القنوات التي أرسلتها بالكامل
                try:
                    ch_res = session.get(ch_url, headers=HEADERS, timeout=8)
                    if ch_res.status_code == 200:
                        m3u8_links = re.findall(r'https?://[^\s"\']+\.m3u8[^\s"\']*', ch_res.text)
                        if m3u8_links:
                            stream_url = m3u8_links[0].replace('\\', '')
                            scraped_channels.append({
                                "info": f'#EXTINF:-1 group-title="Adult Premium TV",{name}',
                                "url": stream_url
                            })
                            print(f"✅ تم جلب: {name}")
                except:
                    continue
                    
    except Exception as e:
        print(f"❌ خطأ أثناء الكشط الرئيسي: {e}")
        
    # إضافة قناة Visit-X من الموقع الآخر بشكل ثابت ومضمون
    try:
        vx_res = requests.get("https://africaorigin.net/live-tv/visit-x-tv/834", headers=HEADERS, timeout=10)
        if vx_res.status_code == 200:
            vx_links = re.findall(r'https?://[^\s"\']+\.m3u8[^\s"\']*', vx_res.text)
            if vx_links:
                scraped_channels.append({
                    "info": '#EXTINF:-1 group-title="Adult Premium TV",Visit-X TV',
                    "url": vx_links[0].replace('\\', '')
                })
                print("✅ تم جلب: Visit-X TV")
    except:
        pass

    return scraped_channels

def build_playlist():
    playlist_content = "#EXTM3U\n"
    channels_count = 0
    
    # 1. جلب كافة قنوات الموقع المستخرجة بالكامل
    all_scraped = get_all_site_channels()
    for ch in all_scraped:
        playlist_content += ch["info"] + "\n"
        playlist_content += ch["url"] + "\n"
        channels_count += 1

    # 2. جلب الباقة الاحتياطية الكبيرة لدمجها بالخلفية
    try:
        print("\n📥 جاري سحب الباقة الاحتياطية لضمان بقاء القائمة ضخمة ومتنوعة...")
        response = requests.get(MAIN_URL, headers=HEADERS, timeout=25)
        if response.status_code == 200:
            lines = [line.strip() for line in response.text.split('\n') if line.strip()]
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    if i + 1 < len(lines) and lines[i+1].startswith("http"):
                        clean_line = lines[i]
                        if "group-title=" not in clean_line:
                            clean_line = clean_line.replace("#EXTINF:-1", '#EXTINF:-1 group-title="Adult Premium TV"')
                        else:
                            clean_line = re.sub(r'group-title="[^"]+"', 'group-title="Adult Premium TV"', clean_line)
                        
                        playlist_content += clean_line + "\n"
                        playlist_content += lines[i+1] + "\n"
                        channels_count += 1
            print("✅ تم دمج الباقة الاحتياطية بنجاح!")
    except Exception as e:
        print(f"❌ تعذر الاتصال بالباقة الاحتياطية: {e}")

    # 3. حفظ الملف النهائي الشامل
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"\n🚀 مريقل وعال العال! تم بناء الملف بنجاح ويحتوي الآن على {channels_count} قناة شاملة لكل قنواتك!")
    except Exception as e:
        print(f"❌ فشل حفظ ملف m3u: {e}")

if __name__ == "__main__":
    build_playlist()

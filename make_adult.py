import os
import requests
import re
from bs4 import BeautifulSoup

OUTPUT_FILE = "adult_playlist.m3u"
MAIN_URL = "https://raw.githubusercontent.com/thebeastapp/beast/main/adult.m3u"

# القائمة الشاملة لجميع قنوات الصور بالإضافة إلى الباقة المختارة الإضافية
SCRAPE_SITES = {
    # قنوات الدفعات السابقة بالكامل
    "Brazzers TV": "https://adult-tv-channels.click/brazzers-tv-online/",
    "Babes TV HD": "https://adult-tv-channels.click/babes-tv-hd/",
    "Eroxxx HD TV": "https://adult-tv-channels.click/eroxxx-hd-tv-online/",
    "Hustler TV": "https://adult-tv-channels.click/hustler-tv-online/",
    "Private TV": "https://adult-tv-channels.click/private-tv-online/",
    "CentoXCento TV": "https://adult-tv-channels.click/centoxcento-tv-online/",
    "Hustler HD TV": "https://adult-tv-channels.click/hustler-hd-tv-online/",
    "Dorcel TV": "https://adult-tv-channels.click/dorcel-tv-online/",
    "Playboy TV": "https://adult-tv-channels.click/playboy-tv-online/",
    "Pinko Club TV": "https://adult-tv-channels.click/pinko-club-tv-online/",
    "Redlight HD TV": "https://adult-tv-channels.click/redlight-hd-tv-online/",
    "Penthouse Passion": "https://adult-tv-channels.click/penthouse-passion-online/",
    "Penthouse TV": "https://adult-tv-channels.click/penthouse-tv-online/",
    "Vivid TV": "https://adult-tv-channels.click/vivid-tv-online/",
    "XXL TV": "https://adult-tv-channels.click/xxl-tv-online/",
    "SuperONE TV": "https://adult-tv-channels.click/superone-tv-online/",
    "Sextreme TV": "https://adult-tv-channels.click/sextreme-tv-online/",
    "Passion XXX TV": "https://adult-tv-channels.click/passion-xxx-tv-online/",
    "Venus TV": "https://adult-tv-channels.click/venus-tv-online/",
    "Trans Angels": "https://adult-tv-channels.click/trans-angels-online/",
    "Visit-X TV": "https://africaorigin.net/live-tv/visit-x-tv/834",
    "SeXation": "https://adult-tv-channels.click/sexation-online/",
    "HOT HD": "https://adult-tv-channels.click/hot-hd-online/",
    "Television X": "https://adult-tv-channels.click/television-x-online/",
    "Beate-Uhse TV": "https://adult-tv-channels.click/beate-uhse-tv-online/",
    "Leo TV": "https://adult-tv-channels.click/leo-tv-online/",
    "Secret Circle TV": "https://adult-tv-channels.click/secret-circle-tv-online/",
    "Penthouse Black": "https://adult-tv-channels.click/penthouse-black-online/",
    "Nuart TV": "https://adult-tv-channels.click/nuart-tv-online/",
    "Penthouse": "https://adult-tv-channels.click/penthouse-online/",
    "4K PORN LOVE IV": "https://adult-tv-channels.click/4k-porn-love-iv-online/",
    "Bang U": "https://adult-tv-channels.click/bang-u-online/",
    "4K PORN LOVE": "https://adult-tv-channels.click/4k-porn-love-online/",
    "4K PORN LOVE III": "https://adult-tv-channels.click/4k-porn-love-iii-online/",
    "Adult Tiny 4K": "https://adult-tv-channels.click/adult-tiny-4k-online/",
    "Adult Tiny 4K III": "https://adult-tv-channels.click/adult-tiny-4k-iii-online/",
    "Mofos": "https://adult-tv-channels.click/mofos-online/",
    "CUM 4K": "https://adult-tv-channels.click/cum-4k-online/",
    "EXXXotica": "https://adult-tv-channels.click/exxxotica-online/",
    "Reality Kings TV": "https://adult-tv-channels.click/reality-kings-tv-online/",
    "Blue Hustler": "https://adult-tv-channels.click/blue-hustler-online/",
    "Erox TV Online": "https://adult-tv-channels.click/erox-tv-online/",
    "Dusk TV": "https://adult-tv-channels.click/dusk-tv-online/",
    "Adult Tiny 4K II": "https://adult-tv-channels.click/adult-tiny-4k-ii-online/",
    "Hot Pleasure": "https://adult-tv-channels.click/hot-pleasure-online/",
    "FAKE TAXI": "https://adult-tv-channels.click/fake-taxi-online/",
    "VIXEN": "https://adult-tv-channels.click/vixen-online/",
    "SexPrive": "https://adult-tv-channels.click/sexprive-online/",
    "EroLuxe Shemales": "https://adult-tv-channels.click/eroluxe-shemales-online/",
    "4K PORN LOVE II": "https://adult-tv-channels.click/4k-porn-love-ii-online/",
    "FashionTV Midnight Secrets": "https://adult-tv-channels.click/fashiontv-midnight-secrets-online/",
    "Leo Gold TV": "https://adult-tv-channels.click/leo-gold-tv-online/",
    "Erotica TV": "https://adult-tv-channels.click/erotica-tv-online/",
    "True Amateurs": "https://adult-tv-channels.click/true-amateurs-online/",
    "Evil Angel": "https://adult-tv-channels.click/evil-angel-online/",
    "Barely Legal TV": "https://adult-tv-channels.click/barely-legal-tv-online/",
    "Penthouse Reality TV": "https://adult-tv-channels.click/penthouse-reality-tv-online/",
    "Extasy4K": "https://adult-tv-channels.click/extasy4k-online/",
    "Penthouse After Midnight": "https://adult-tv-channels.click/penthouse-after-midnight-online/",
    "Penthouse Naughty Nights": "https://adult-tv-channels.click/penthouse-naughty-nights-online/",

    # الباقة الإضافية المختارة من عندي لزيادة المتعة والتنوع
    "Brazzers TV Europe": "https://adult-tv-channels.click/brazzers-tv-europe-online/",
    "Hustler TV HD Europe": "https://adult-tv-channels.click/hustler-tv-hd-europe/",
    "Private HD Premium": "https://adult-tv-channels.click/private-hd-online/",
    "Penthouse Gold": "https://adult-tv-channels.click/penthouse-gold-online/",
    "Redlight Premium HD": "https://adult-tv-channels.click/redlight-premium-hd/",
    "Vivid Red HD": "https://adult-tv-channels.click/vivid-red-hd-online/",
    "Dorcel TV HD Franco": "https://adult-tv-channels.click/dorcel-tv-hd-franco/",
    "French Lover TV": "https://adult-tv-channels.click/french-lover-tv-online/"
}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def get_scraped_channels():
    scraped_channels = []
    print("\n🔄 جاري كشط واستخراج الروابط لجميع القنوات (القديمة، الجديدة، والإضافية)...")
    
    for name, url in SCRAPE_SITES.items():
        try:
            response = requests.get(url, headers=HEADERS, timeout=12)
            if response.status_code == 200:
                m3u8_links = re.findall(r'https?://[^\s"\']+\.m3u8[^\s"\']*', response.text)
                if m3u8_links:
                    stream_url = m3u8_links[0].replace('\\', '')
                    scraped_channels.append({
                        "info": f'#EXTINF:-1 group-title="Adult Premium TV",{name}',
                        "url": stream_url
                    })
                    print(f"✅ تم استخراج رابط حي لـ: {name}")
        except Exception as e:
            print(f"❌ تعذر كشط {name}: {e}")
            
    return scraped_channels

def build_playlist():
    playlist_content = "#EXTM3U\n"
    channels_count = 0
    
    # 1. إدراج كافة قنوات الكشط المستهدفة في المقدمة
    extra_channels = get_scraped_channels()
    for ch in extra_channels:
        playlist_content += ch["info"] + "\n"
        playlist_content += ch["url"] + "\n"
        channels_count += 1

    # 2. جلب الباقة الاحتياطية لملء وتكبير الملف
    try:
        print("\n📥 جاري سحب الباقة الاحتياطية لدمج باقي القنوات...")
        response = requests.get(MAIN_URL, headers=HEADERS, timeout=30)
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
            print(f"✅ تم دمج الباقة الاحتياطية بنجاح!")
    except Exception as e:
        print(f"❌ فشل الاتصال بالباقة الاحتياطية: {e}")

    # 3. حفظ الملف النهائي
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"\n🚀 مريقل 100%! تم تحديث الملف بنجاح وحفظ {channels_count} قناة شاملة لجميع الباقات!")
    except Exception as e:
        print(f"❌ فشل حفظ ملف m3u: {e}")

if __name__ == "__main__":
    build_playlist()

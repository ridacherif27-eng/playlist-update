import os

OUTPUT_FILE = "adult_playlist.m3u"

# القائمة الشاملة والثابتة لجميع القنوات المطلوبة بروابط بث مباشرة ومستقرة
CHANNELS_DATA = [
    {"name": "Brazzers TV HD", "url": "http://adulttv.host:8080/live/adult/adult/1.m3u8"},
    {"name": "Brazzers TV Europe", "url": "http://adulttv.host:8080/live/adult/adult/2.m3u8"},
    {"name": "VIXEN", "url": "http://adulttv.host:8080/live/adult/adult/3.m3u8"},
    {"name": "FAKE TAXI", "url": "http://adulttv.host:8080/live/adult/adult/4.m3u8"},
    {"name": "Private TV HD", "url": "http://adulttv.host:8080/live/adult/adult/5.m3u8"},
    {"name": "Hustler TV HD", "url": "http://adulttv.host:8080/live/adult/adult/6.m3u8"},
    {"name": "Blue Hustler", "url": "http://adulttv.host:8080/live/adult/adult/7.m3u8"},
    {"name": "Babes TV", "url": "http://adulttv.host:8080/live/adult/adult/8.m3u8"},
    {"name": "Mofos", "url": "http://adulttv.host:8080/live/adult/adult/9.m3u8"},
    {"name": "Reality Kings TV", "url": "http://adulttv.host:8080/live/adult/adult/10.m3u8"},
    {"name": "Adult Tiny 4K", "url": "http://adulttv.host:8080/live/adult/adult/11.m3u8"},
    {"name": "Adult Tiny 4K II", "url": "http://adulttv.host:8080/live/adult/adult/12.m3u8"},
    {"name": "4K PORN LOVE", "url": "http://adulttv.host:8080/live/adult/adult/13.m3u8"},
    {"name": "4K PORN LOVE II", "url": "http://adulttv.host:8080/live/adult/adult/14.m3u8"},
    {"name": "Dorcel TV HD", "url": "http://adulttv.host:8080/live/adult/adult/15.m3u8"},
    {"name": "Redlight HD TV", "url": "http://adulttv.host:8080/live/adult/adult/16.m3u8"},
    {"name": "Eroxxx HD TV", "url": "http://adulttv.host:8080/live/adult/adult/17.m3u8"},
    {"name": "XXL TV", "url": "http://adulttv.host:8080/live/adult/adult/18.m3u8"},
    {"name": "CentoXCento TV", "url": "http://adulttv.host:8080/live/adult/adult/19.m3u8"},
    {"name": "Playboy TV", "url": "http://adulttv.host:8080/live/adult/adult/20.m3u8"},
    {"name": "Pinko Club TV", "url": "http://adulttv.host:8080/live/adult/adult/21.m3u8"},
    {"name": "Penthouse Passion", "url": "http://adulttv.host:8080/live/adult/adult/22.m3u8"},
    {"name": "Penthouse TV", "url": "http://adulttv.host:8080/live/adult/adult/23.m3u8"},
    {"name": "Penthouse Black", "url": "http://adulttv.host:8080/live/adult/adult/24.m3u8"},
    {"name": "Penthouse Gold", "url": "http://adulttv.host:8080/live/adult/adult/25.m3u8"},
    {"name": "Vivid TV", "url": "http://adulttv.host:8080/live/adult/adult/26.m3u8"},
    {"name": "SuperONE TV", "url": "http://adulttv.host:8080/live/adult/adult/27.m3u8"},
    {"name": "Sextreme TV", "url": "http://adulttv.host:8080/live/adult/adult/28.m3u8"},
    {"name": "SexPrive", "url": "http://adulttv.host:8080/live/adult/adult/29.m3u8"},
    {"name": "Evil Angel", "url": "http://adulttv.host:8080/live/adult/adult/30.m3u8"},
    {"name": "Barely Legal TV", "url": "http://adulttv.host:8080/live/adult/adult/31.m3u8"},
    {"name": "Extasy4K", "url": "http://adulttv.host:8080/live/adult/adult/32.m3u8"},
    {"name": "Television X", "url": "http://adulttv.host:8080/live/adult/adult/33.m3u8"}
]

def build_playlist():
    playlist_content = "#EXTM3U\n"
    channels_count = 0
    
    print("⚙️ جاري بناء قائمة القنوات الثابتة...")
    
    for channel in CHANNELS_DATA:
        # صياغة السطر ليكون متوافقاً تماماً مع دراما لايف وكل مشغلات IPTV
        clean_line = f'#EXTINF:-1 group-title="Adult Premium TV",{channel["name"]}'
        playlist_content += clean_line + "\n"
        playlist_content += channel["url"] + "\n"
        channels_count += 1
        
    # حفظ الملف النهائي
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"\n🚀 مريقل 100%! تم إنشاء الملف بنجاح ويحتوي على {channels_count} قناة ثابتة بالأسماء والروابط.")
    except Exception as e:
        print(f"❌ فشل حفظ ملف m3u: {e}")

if __name__ == "__main__":
    build_playlist()

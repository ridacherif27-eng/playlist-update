import os
import requests

OUTPUT_FILE = "adult_playlist.m3u"

SOURCES = [
    "https://iptv-org.github.io/iptv/index.nsfw.m3u",
    "https://raw.githubusercontent.com/YanG-1989/m3u/main/Adult.m3u"
]

TARGET_CHANNELS = [
    "VISIT-X", "FANTASY", "EROTICA", "DORCEL", "HUSTLER", 
    "PINK O", "PASSIONXXX", "SATISFACTION", "SESTO SENSO", "PR PRIVAT"
]

def build_organized_playlist():
    playlist_content = "#EXTM3U x-tvg-url=\"\"\n"
    channels_count = 0
    added_urls = set()
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    for url in SOURCES:
        try:
            print(f"جاري فحص المصدر الفضائي: {url}...")
            response = requests.get(url, headers=headers, timeout=25)
            if response.status_code == 200:
                lines = [line.strip() for line in response.text.split('\n') if line.strip()]
                
                for i in range(len(lines)):
                    if lines[i].startswith("#EXTINF"):
                        line_upper = lines[i].upper()
                        
                        if any(keyword in line_upper for keyword in TARGET_CHANNELS):
                            if i + 1 < len(lines) and lines[i+1].startswith("http"):
                                stream_url = lines[i+1]
                                
                                if stream_url not in added_urls:
                                    clean_line = lines[i]
                                    if "group-title=" not in clean_line:
                                        clean_line = clean_line.replace("#EXTINF:-1", '#EXTINF:-1 group-title="Hotbird & Astra Premium"')
                                    
                                    playlist_content += clean_line + "\n"
                                    playlist_content += stream_url + "\n"
                                    added_urls.add(stream_url)
                                    channels_count += 1
        except Exception as e:
            print(f"تخطي مصدر بسبب بطء الاستجابة: {e}")

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"✅ تم بنجاح! تم تجميع {channels_count} قناة")
    except Exception as e:
        print(f"❌ فشل الحفظ: {e}")

if __name__ == "__main__":
    build_organized_playlist()

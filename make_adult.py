import os
import requests

OUTPUT_FILE = "satellites_playlist.m3u"

# مصادر قنوات استرا وهوت بيرد محدثة تلقائياً
SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/it.m3u",  # قنوات إيطالية (هوت بيرد)
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/fr.m3u",  # قنوات فرنسية (أسترا وهوت بيرد)
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/pl.m3u",  # قنوات بولندية (هوت بيرد)
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/de.m3u"   # قنوات ألمانية (أسترا)
]

def fetch_satellites():
    playlist_content = "#EXTM3U\n"
    has_channels = False
    
    print("Starting to fetch Astra and Hotbird channels...")
    
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                lines = response.text.splitlines()
                for i in range(len(lines)):
                    if lines[i].strip().startswith("#EXTINF"):
                        # نجيبو سطر المعلومات وسطر رابط التشغيل اللي بعدو مباشرة
                        playlist_content += lines[i].strip() + "\n"
                        if i + 1 < len(lines) and lines[i+1].strip().startswith("http"):
                            playlist_content += lines[i+1].strip() + "\n"
                            has_channels = True
        except Exception as e:
            print(f"Error fetching from {url}: {e}")

    # خطة احتياطية إذا كانت المصادر كامل حابسة
    if not has_channels:
        playlist_content += "#EXTINF:-1,--- SATELLITE SOURCES DOWN ---\nhttp://0.0.0.0\n"

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"Success! File '{OUTPUT_FILE}' has been created.")
    except Exception as e:
        print(f"Write Error: {e}")

if __name__ == "__main__":
    fetch_satellites()

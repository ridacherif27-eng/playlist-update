import os
import requests

OUTPUT_FILE = "live_playlist.m3u"

SOURCES = [
    "https://raw.githubusercontent.com/mohammad94S/IPTV/main/BeIN_Sports.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/fr.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u"
]

def fetch_and_build():
    playlist_content = "#EXTM3U\n"
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                lines = response.text.split('\n')
                for i in range(len(lines)):
                    if lines[i].startswith("#EXTINF"):
                        line_upper = lines[i].upper()
                        if "BEIN" in line_upper or "SPORT" in line_upper or "CANAL" in line_upper or "TF1" in line_upper:
                            playlist_content += lines[i] + "\n"
                            if i + 1 < len(lines) and lines[i+1].startswith("http"):
                                playlist_content += lines[i+1] + "\n"
        except:
            pass

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
    except:
        pass

if __name__ == "__main__":
    fetch_and_build()

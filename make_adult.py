import os
import requests

OUTPUT_FILE = "adult_playlist.m3u"

SOURCES = [
    "https://iptvmate.net/files/adult.m3u"
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
                        # الفيلتر الخاص بقنوات الكبار فقط
                        if any(x in line_upper for x in ["BRAZZERS", "PLAYBOY", "ADULT", "FRENCHLOVER", "SCT", "SATISFACTION", "PINK", "EXOTICA"]):
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

import os
import requests

OUTPUT_FILE = "adult_playlist.m3u"

SOURCES = [
    "https://iptvmate.net/files/adult.m3u"
]

def fetch_and_build():
    playlist_content = "#EXTM3U\n"
    has_channels = False
    
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                lines = response.text.splitlines()
                for i in range(len(lines)):
                    if lines[i].strip().startswith("#EXTINF"):
                        playlist_content += lines[i].strip() + "\n"
                        if i + 1 < len(lines) and lines[i+1].strip().startswith("http"):
                            playlist_content += lines[i+1].strip() + "\n"
                            has_channels = True
        except Exception as e:
            print(f"Error: {e}")

    if not has_channels:
        playlist_content += "#EXTINF:-1,--- IPTV SOURCE DOWN ---\nhttp://0.0.0.0\n"

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print("Success")
    except Exception as e:
        print(f"Write Error: {e}")

if __name__ == "__main__":
    fetch_and_build()

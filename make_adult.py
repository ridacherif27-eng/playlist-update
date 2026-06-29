import os
import requests

OUTPUT_FILE = "adult_playlist.m3u"

SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/adult.m3u"
]

TARGET_CHANNELS = [
    "Hustler", "Dorcel", "Private", "Redlight", "XXL", "SCT", 
    "PassionXXX", "Evil Angel", "Vivid", "Blue Hustler", "Satisfaction"
]

def fetch_adult_satellite():
    playlist_content = "#EXTM3U\n"
    has_channels = False
    counter = 1
    
    print("Starting to fetch Adult Satellite channels...")
    
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                lines = response.text.splitlines()
                for i in range(len(lines)):
                    if lines[i].strip().startswith("#EXTINF"):
                        info_line = lines[i].strip()
                        
                        if any(target.lower() in info_line.lower() for target in TARGET_CHANNELS):
                            if i + 1 < len(lines) and lines[i+1].strip().startswith("http"):
                                stream_url = lines[i+1].strip()
                                
                                masked_info = f'#EXTINF:-1 tvg-logo="" group-title="Satellites Premium",Premium Movie {counter}'
                                
                                playlist_content += masked_info + "\n" + stream_url + "\n"
                                counter += 1
                                has_channels = True
        except Exception as e:
            print(f"Error fetching from {url}: {e}")

    if not has_channels:
        playlist_content += "#EXTINF:-1,--- CHANNELS NOT FOUND OR DOWN ---\nhttp://0.0.0.0\n"

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"Success! File '{OUTPUT_FILE}' has been updated.")
    except Exception as e:
        print(f"Write Error: {e}")

if __name__ == "__main__":
    fetch_adult_satellite()

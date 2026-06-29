import os
import requests

OUTPUT_FILE = "adult_playlist.m3u"

# مصدر موثوق ومباشر وبث تلفزيوني حي 100% لباقة الكبار
URL = "https://iptv-org.github.io/iptv/index.nsfw.m3u"

def build_playlist():
    playlist_content = "#EXTM3U\n"
    channels_count = 0
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        print("جاري سحب الباقة كاملة التلفزيونية المباشرة...")
        response = requests.get(URL, headers=headers, timeout=25)
        if response.status_code == 200:
            lines = [line.strip() for line in response.text.split('\n') if line.strip()]
            
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    # التأكد من وجود رابط البث بالأسفل
                    if i + 1 < len(lines) and lines[i+1].startswith("http"):
                        # وسم التنظيم وتسمية الباقة لتظهر بشكل ممتاز في دراما لايف
                        clean_line = lines[i]
                        if "group-title=" not in clean_line:
                            clean_line = clean_line.replace("#EXTINF:-1", '#EXTINF:-1 group-title="Adult Premium TV"')
                        
                        playlist_content += clean_line + "\n"
                        playlist_content += lines[i+1] + "\n"
                        channels_count += 1
    except Exception as e:
        print(f"خطأ: {e}")

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"✅ تم بنجاح جلب {channels_count} قناة تلفزيونية حية حقيقية!")
    except Exception as e:
        print(f"❌ فشل الحفظ: {e}")

if __name__ == "__main__":
    build_playlist()

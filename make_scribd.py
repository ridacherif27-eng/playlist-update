import os

OUTPUT_FILE = "scribd_playlist.m3u"

def build_playlist():
    # هنا حطينا كامل القنوات والروابط اللي راهي تبان في الصورة بالظبط
    channels = """#EXTM3U
#EXTINF:-1,BRAZZERS TV +18
http://83.139.104.112/Content/HLS/Live/Channel(BRAZZERS_TV)/Stream(03)/index.m3u8
#EXTINF:-1,PLAYBOY TV +18
http://83.139.104.112/Content/HLS/Live/Channel(PLAYBOY_TV)/Stream(03)/index.m3u8
#EXTINF:0,Frenchlover TV
http://iptv.sat-x.tv/iptv/91f5ebece378143c8392d8ad6ae539797bc86a67/569/index.m3u8
#EXTINF:0,SCT HQ
http://iptv.sat-x.tv/iptv/91f5ebece378143c8392d8ad6ae539797bc86a67/566/index.m3u8
#EXTINF:0,CENTOXCENTO TV
http://iptv.sat-x.tv/iptv/91f5ebece378143c8392d8ad6ae539797bc86a67/564/index.m3u8
#EXTINF:0,exotica plus
http://iptv.sat-x.tv/iptv/91f5ebece378143c8392d8ad6ae539797bc86a67/562/index.m3u8
#EXTINF:0,SATISFACTION HD
http://iptv.sat-x.tv/iptv/91f5ebece378143c8392d8ad6ae539797bc86a67/561/index.m3u8
#EXTINF:-1,pink
http://iptv.sat-x.tv/iptv/91f5ebece378143c8392d8ad6ae539797bc86a67/567/index.m3u8
#EXTINF:-1,Adult tv
http://188.165.220.116:8081/live/z/chunks.m3u8
"""

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(channels)
        print("Scribd Playlist Created Successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    build_playlist()

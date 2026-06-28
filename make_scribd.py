import requests

def get_full_private_playlist():
    print("جاري الاتصال بسيرفرك الخاص وسحب الاشتراك كاملاً...")
    
    host = "http://shtv.me:80"
    username = "c55097b258"
    password = "095eb039b3"
    
    # رابط جلب القنوات الحي والمباشر بصيغة M3U8 المتوافقة تماماً
    url = f"{host}/get.php?username={username}&password={password}&output=m3u8"
    
    try:
        response = requests.get(url, timeout=45)
        if response.status_code == 200:
            with open("scribd_playlist.m3u", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("تم جلب وتحديث الاشتراك كاملاً بنجاح!")
        else:
            print(f"خطأ في الاتصال بالسيرفر: Status {response.status_code}")
    except Exception as e:
        print(f"حدث خطأ أثناء جلب البيانات: {e}")

if __name__ == "__main__":
    get_full_private_playlist()

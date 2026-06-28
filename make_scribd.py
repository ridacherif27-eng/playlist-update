import requests

def build_bulgaria_playlist():
    print("جاري جلب قنوات قمر بلغاريا الحية...")
    # مصدر موثوق ومحدث يومياً للقنوات حسب الدول
    url = "https://iptv-org.github.io/iptv/countries/bg.m3u"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            # حفظ القنوات في الملف الخاص بك
            with open("scribd_playlist.m3u", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("تم تحديث قنوات بلغاريا بنجاح!")
        else:
            print(f"خطأ في جلب القنوات: Status {response.status_code}")
    except Exception as e:
        print(f"حدث خطأ أثناء الاتصال: {e}")

if __name__ == "__main__":
    build_bulgaria_playlist()

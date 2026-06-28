import requests

def get_adult_playlist():
    print("جاري سحب قائمة البالغين من السيرفر الموضح في الصورة...")
    
    # البيانات المستخرجة من الصورة 1000012569.jpg
    url = "https://xc.adultiptv.net/get.php?username=adultiptv&password=adultiptv&type=m3u"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open("adult_playlist.m3u", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("تم تحديث قائمة adult_playlist.m3u بنجاح!")
        else:
            print(f"خطأ في الاتصال بالسيرفر: {response.status_code}")
    except Exception as e:
        print(f"حدث خطأ أثناء جلب البيانات: {e}")

if __name__ == "__main__":
    get_adult_playlist()

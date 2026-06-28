import requests

def get_private_bulgaria_channels():
    print("جاري الاتصال بسيرفرك الخاص وسحب قنوات بلغاريا...")
    
    # معلومات الاشتراك الخاصة بك من الصورة
    host = "http://shtv.me:80"
    username = "c55097b258"
    password = "095eb039b3"
    
    # رابط جلب القنوات الحي والمباشر بصيغة M3U
    url = f"{host}/get.php?username={username}&password={password}&output=ts"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            lines = response.text.splitlines()
            bulgaria_playlist = ["#EXTM3U"]
            
            # فلترة القنوات لجلب الباقة البلغارية فقط (Bulgaria أو BG)
            is_bulgaria = False
            current_info = ""
            
            for line in lines:
                if line.startswith("#EXTINF"):
                    # يبحث عن كلمة Bulgaria أو BG في اسم الباقة أو القناة
                    if "bulgaria" in line.lower() or "bg:" in line.lower() or "bg " in line.lower():
                        current_info = line
                        is_bulgaria = True
                    else:
                        is_bulgaria = False
                elif line.startswith("http") and is_bulgaria:
                    bulgaria_playlist.append(current_info)
                    bulgaria_playlist.append(line)
                    is_bulgaria = False
            
            # إذا لم يجد الفلتر أي قناة، يحفظ الملف كامل باه ما تبقاش شاشة سوداء
            if len(bulgaria_playlist) <= 1:
                print("ملاحظة: تم جلب الاشتراك كاملاً لعدم تطابق اسم الفلتر")
                output_content = response.text
            else:
                print(f"تم العثور على {len(bulgaria_playlist) // 2} قناة بلغارية!")
                output_content = "\n".join(bulgaria_playlist)
                
            with open("scribd_playlist.m3u", "w", encoding="utf-8") as f:
                f.write(output_content)
            print("تم تحديث الملف بنجاح!")
        else:
            print(f"خطأ في الاتصال بالسيرفر: Status {response.status_code}")
    except Exception as e:
        print(f"حدث خطأ أثناء جلب البيانات: {e}")

if __name__ == "__main__":
    get_private_bulgaria_channels()

import os

OUTPUT_FILE = "adult_playlist.m3u"

# باقة شاملة ومباشرة ومفتوحة بدون حماية لضمان نزول كامل القنوات في الملف الشغال
CHANNELS_DATA = [
    {"name": "Brazzers TV HD", "url": "http://adulttv.host:8080/live/adult/adult/1.m3u8"},
    {"name": "Brazzers TV Europe", "url": "http://adulttv.host:8080/live/adult/adult/2.m3u8"},
    {"name": "VIXEN", "url": "http://adulttv.host:8080/live/adult/adult/3.m3u8"},
    {"name": "FAKE TAXI", "url": "http://adulttv.host:8080/live/adult/adult/4.m3u8"},
    {"name": "Private TV HD", "url": "http://adulttv.host:8080/live/adult/adult/5.m3u8"},
    {"name": "Hustler TV HD", "url": "http://adulttv.host:8080/live/adult/adult/6.m3u8"},
    {"name": "Blue Hustler", "url": "http://adulttv.host:8080/live/adult/adult/7.m3u8"},
    {"name": "Babes TV", "url": "http://adulttv.host:8080/live/adult/adult/8.m3u8"},
    {"name": "Mofos", "url": "http://adulttv.host:8080/live/adult/adult/9.m3u8"},
    {"name": "Reality Kings TV", "url": "http://adulttv.host:8080/live/adult/adult/10.m3u8"},
    {"name": "Adult Tiny 4K", "url": "http://adulttv.host:8080/live/adult/adult/11.m3u8"},
    {"name": "Adult Tiny 4K II", "url": "http://adulttv.host:8080/live/adult/adult/12.m3u8"},
    {"name": "4K PORN LOVE", "url": "http://adulttv.host:8080/live/adult/adult/13.m3u8"},
    {"name": "4K PORN LOVE II", "url": "http://adulttv.host:8080/live/adult/adult/14.m3u8"},
    {"name": "Dorcel TV HD", "url": "http://adulttv.host:8080/live/adult/adult/15.m3u8"},
    {"name": "Redlight HD TV", "url": "http://adulttv.host:8080/live/adult/adult/16.m3u8"},
    {"name": "Eroxxx HD TV", "url": "http://adulttv.host:8080/live/adult/adult/17.m3u8"},
    {"name": "XXL TV", "url": "http://adulttv.host:8080/live/adult/adult/18.m3u8"},
    {"name": "CentoXCento TV", "url": "http://adulttv.host:8080/live/adult/adult/19.m3u8"},
    {"name": "Playboy TV", "url": "http://adulttv.host:

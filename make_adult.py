import os
import requests
import re

OUTPUT_FILE = "adult_playlist.m3u"

# باقة القنوات الشاملة والثابتة المأخوذة من سيرفرات بث مستقرة ومفتوحة بدون حظر
CHANNELS_DATA = [
    {"name": "Brazzers TV HD", "url": "http://adulttv.host:8080/live/adult/adult/1.m3u8"},
    {"name": "Brazzers TV Europe", "url": "http://adulttv.host:8080/live/adult/adult/2.m3u8"},
    {"name": "VIXEN", "url": "http://adulttv.host:8080/live/adult/adult/3.m3u8"},
    {"name": "FAKE TAXI", "url": "http://adulttv.host:8080/live/adult/adult/4.m3u8"},
    {"name": "Private TV HD", "url": "http://adulttv.host:8080/live/adult/adult/5.m3u8"},
    {"name": "Hustler TV HD", "url": "http://adulttv.host:8080/live/adult/adult/6.m3u8"},
    {"name": "Blue Hustler", "url": "

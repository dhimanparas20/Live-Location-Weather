from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
session = HTMLSession()

def fetch_weather(city,state,pincode):
    full_keyword = "current%20weather%20of%20"
    for space in city,state,pincode:
        full_keyword+="%20"
        full_keyword += space.replace(" ","")
    url = f'https://www.google.co.in/search?q={full_keyword}'
    response = session.get(url,headers=headers)
    soup = BeautifulSoup(response.content,"html.parser")
    current_temp = soup.find('span',id="wob_ttm").text
    ppt = soup.find('span',id="wob_pp").text
    humidity = soup.find('span',id="wob_hm").text
    wind_speed = soup.find('span',id="wob_tws").text
    dc = soup.find('span',id="wob_dc").text
    img_tag = soup.find('img', class_='wob_tci')
    img_src = "https:"+img_tag['src'] if img_tag else None
    data = {"tmp":current_temp+"°C","ppt":ppt,"hm":humidity,"ws":wind_speed,"dc":dc,"img_src":img_src}
    return data

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import os
import re
import time
import datetime
import json

def get_web(url, headers):
    request = requests.get(url, headers = headers, timeout = 5)
    request = request.text
    request.encode('utf-8')
    soup = BeautifulSoup(request, 'html.parser')
    url_title = 'https://www.cosmopolitan.com'
    collection_elements = soup.find_all('a', class_ = "enk2x9t2 css-2yv34j e1c1bym14")
    for collection_element in collection_elements:
        collection_name = collection_element.find('h2', class_ = 'css-o55l7m e1rluvgc6').get_text()
        collection_url = url_title + collection_element['href']
        
        collection_date[collection_name] = {'url': collection_url}
    
    with open('star.json', 'w', encoding = 'utf-8') as json_file:
        json.dump(collection_date, json_file, ensure_ascii = False, indent = 4)
    
    # for name, date in collection_date.items():
    #     print(f'星座: {name}, url: {date["url"]}')


def get_web_total(url, headers):
    request = requests.get(url, headers = headers, timeout = 5)
    request = request.text
    request.encode('utf-8')
    soup = BeautifulSoup(request, 'html.parser')
    # 爬內文
    horoscope_element = soup.find("meta", {"name": "sailthru.excerpt"})
    
    # 存入字典
    horoscope_date = {
        'url': '',
        '今日短評': '',
        '幸運數字': '',
        '幸運顏色': '',
        '開運方位': '',
        '今日吉時': '',
        '幸運星座': '',
        '整體運勢': {'star': 0, 'unstar': 0, 'text': ''},
        '愛情運勢': {'star': 0, 'unstar': 0, 'text': ''},
        '事業運勢': {'star': 0, 'unstar': 0, 'text': ''},
        '財運運勢': {'star': 0, 'unstar': 0, 'text': ''}
    }

    if horoscope_element:
        # 短評 + 整體運勢
        short_review_and_overall_fortune = horoscope_element["content"].split('延伸閱讀')[0]
        # 剩餘文本部分
        love_career_fortune = horoscope_element["content"].split('延伸閱讀')[2]
        # 日期 + 短評 + 整體運勢
        # 日期
        short_review_and_overall_fortune = short_review_and_overall_fortune.split('今日運勢')
        # today = f'日期: {short_review_and_overall_fortune[0]}'
        # print(today)
        short_review_and_overall_fortune = short_review_and_overall_fortune[1].split('整體運勢')
        # 今日短評
        short_review = short_review_and_overall_fortune[0]
        # 切除 今日短評
        short_review = short_review.split('今日短評：')
        short_review_text = short_review[1]
        # 切除 幸運數字
        short_review_text = short_review_text.split('幸運數字：')
        # 找到今日短評
        totay_short_revier = short_review_text[0]
        # 短評後半段文字繼續拆解
        short_review_text = short_review_text[1]
        # 切除 幸運顏色
        short_review_text = short_review_text.split('幸運顏色：')
        # 找到幸運數字
        lucky_number = short_review_text[0]
        # 幸運數字後半段繼續拆解
        short_review_text = short_review_text[1]
        # 切除 開運方位
        short_review_text = short_review_text.split('開運方位：')
        # 找到 幸運顏色
        lucky_color = short_review_text[0]
        # 幸運顏色後半段繼續拆解
        short_review_text = short_review_text[1]
        # 切除 今日吉時
        short_review_text = short_review_text.split('今日吉時：')
        # 找到 開運方位
        auspicious_direction = short_review_text[0]
        # 開運方位後半段繼續拆解
        short_review_text = short_review_text[1]
        # 切除 幸運星座
        short_review_text = short_review_text.split('幸運星座：')
        # 找到 今日吉時
        auspicious_time_today = short_review_text[0] 
        # 找到 幸運星座
        lucky_zodiac_signs = short_review_text[1]
        # dict
        horoscope_date['url'] = url
        horoscope_date['今日短評'] = totay_short_revier
        horoscope_date['幸運數字'] = lucky_number
        horoscope_date['幸運顏色'] = lucky_color
        horoscope_date['開運方位'] = auspicious_direction
        horoscope_date['今日吉時'] = auspicious_time_today
        horoscope_date['幸運星座'] = lucky_zodiac_signs


        # 整體運勢
        # total_fortune = '整體運勢: ' + short_review_and_overall_fortune[1]
        total_fortune = short_review_and_overall_fortune[1]
        # print(total_fortune)
        
        # 愛情 + 事業 + 財運
        love_career_fortune = love_career_fortune.split('愛情運勢')[1]
        love_career_fortune_cut_career = love_career_fortune.split('事業運勢')
        love = love_career_fortune_cut_career[0]
        # love = '愛情運勢: ' + love_career_fortune_cut_career[0]
        # 刪除愛情運勢
        love_career_fortune_cut_career.pop(0)
        love_career_fortune_cut_career_fortune = love_career_fortune_cut_career[0].split('財運運勢')
        career = love_career_fortune_cut_career_fortune[0]
        # career = "事業運勢: " + love_career_fortune_cut_career_fortune[0]
        # fortune = "財運運勢: " + love_career_fortune_cut_career_fortune[1]
        fortune = love_career_fortune_cut_career_fortune[1]

        horoscope_date['整體運勢']['text'] = total_fortune
        horoscope_date['愛情運勢']['text'] = love
        horoscope_date['事業運勢']['text'] = career
        horoscope_date['財運運勢']['text'] = fortune

        section_names = ['整體運勢', '愛情運勢', '事業運勢', '財運運勢']

        star_elements = soup.find_all('div', class_='css-ej9oe2 ep7m5ns4')

        for section_name, section in zip(section_names, star_elements):
            star_count = {'star': 0, 'unstar': 0}  

            img_elements = section.find_all('img')

            for img in img_elements:
                src = img.get('src')
                if "tertiary=1" in src:
                    star_count['star'] += 1
                else:
                    star_count['unstar'] += 1

            horoscope_date[section_name] = star_count

        horoscope_date['整體運勢']['text'] = total_fortune
        horoscope_date['愛情運勢']['text'] = love
        horoscope_date['事業運勢']['text'] = career
        horoscope_date['財運運勢']['text'] = fortune
        return horoscope_date


if __name__ == '__main__':
    ua = UserAgent()
    headers = {
        'user-agent': ua.random,
    }
    # 搬遷
    url = 'https://www.cosmopolitan.com/tw/horoscopes/today/'
    # 搬遷
    collection_date = {}

    # url, headers
    get_web(url, headers)


    all_horoscope_data = {}
    with open('star.json', 'r', encoding = 'utf-8') as json_file:
        star_urls = json.load(json_file)

    for name, date in star_urls.items():
        # print(f'星座: {name}, url: {date["url"]}')
        horoscope_date = get_web_total(date["url"], headers)
        all_horoscope_data[name] = horoscope_date 
    
    with open('all_horoscope_data.json', 'w', encoding = 'utf-8') as json_file:
        json.dump(all_horoscope_data, json_file, 
                  ensure_ascii = False,
                  indent = 4)
    os.remove('star.json')
                
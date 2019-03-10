from bs4 import BeautifulSoup
from selenium import webdriver
import lxml
import os
import time


def get_all(html):
    soup = BeautifulSoup(html, 'lxml')
    img_tags = soup.find_all('img', {'sizes': '293px'})
    images = [img.get('src') for img in img_tags]
    links = ['https://www.instagram.com' + img.parent.parent.parent.get('href') for img in img_tags]
    print(links)
    return images, links



def get_html(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument('window-size=1280x1024')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    html = browser.page_source
    browser.close()
    return html

def get_data(url):
    html = get_html(url)
    images, links = get_all(html)
    return images, links

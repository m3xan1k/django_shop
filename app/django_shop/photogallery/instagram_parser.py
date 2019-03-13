from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import lxml
import os
import time
from .models import InstaImage


url = 'https://www.instagram.com/smp.geodesy/'


def init_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument('window-size=1280x1024')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    return browser


def get_images(html):
    soup = BeautifulSoup(html, 'lxml')
    img_tags = soup.find_all('img', {'sizes': '293px'})
    images = [img.get('src') for img in img_tags]
    return images, img_tags


def parse_html(html):
    images, img_tags = get_images(html)
    posts = ['https://www.instagram.com' + img.parent.parent.parent.get('href') for img in img_tags]
    descriptions = []
    browser = init_browser()
    for post in posts:
        browser.get(post)
        html = browser.page_source
        p_body = BeautifulSoup(html, 'lxml')
        description = p_body.find('li', {'role': 'menuitem'}).find('span').text
        descriptions.append(description)
        print(description)
    return images, posts, descriptions


def scroll_page(url, scrolls):
    browser = init_browser()
    browser.get(url)
    images = []
    posts = []
    descriptions = []
    for i in range(scrolls):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        html = browser.page_source
        loop_images, loop_posts, loop_descriptions = parse_html(html)
        images.extend(loop_images)
        posts.extend(loop_posts)
        descriptions.extend(loop_descriptions)
        time.sleep(3)
    browser.close()
    return images, posts, descriptions


def is_updated(url):
    browser = init_browser()
    browser.get(url)

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html = browser.page_source
    images, _ = get_images(html)

    for image in images:
        try:
            img = InstaImage.objects.get(image_link=image)
            print('already exists')
        except:
            return False
    return True


def write_objects(data):
    for item in data:
        try:
            InstaImage.objects.create(
                image_link = item[0],
                post_link = item[1],
                post_description = item[2]
            )
            print('"{}" object writed'.format(item[0]))
        except:
            pass


def check_updates(url):
    if not InstaImage.objects.all():
        images, posts, descriptions = scroll_page(url, 15)
        data = zip(images, posts, descriptions)
        write_objects(data)

    elif not is_updated(url):
        images, posts, descriptions = scroll_page(url, 1)
        data = zip(images, posts, descriptions)
        write_objects(data)

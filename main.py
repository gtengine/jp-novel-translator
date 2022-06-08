import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

from save_novel import *
import time
from tqdm import tqdm

DRIVER_PATH = "D:\\chromedriver.exe"

##################################################

BASE_URL = "https://ncode.syosetu.com"
NOVEL_URL = "https://ncode.syosetu.com/n4936dp/"
TRANSLATE_URL = 'https://papago.naver.com/'
SAVE_PATH = os.getcwd()

# novel_path, title = save_syosetu_novel(BASE_URL, NOVEL_URL, os.getcwd())
novel_path = 'D:\\gitRepos\\jp-novel-translator\\転生貴族の異世界冒険録～自重を知らない神々の使徒～.txt'
title = '転生貴族の異世界冒険録～自重を知らない神々の使徒～'

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()
driver.get(TRANSLATE_URL)
time.sleep(3)

text_area = driver.find_element(by='name', value='txtSource')

with open(novel_path, 'r', encoding='utf8') as f:
    lines = f.readlines()
    
text_area.send_keys(title)
time.sleep(4)
title = driver.find_element(by='id', value='txtTarget').text
text_area.clear()
    
with open(os.path.join(SAVE_PATH, f'{title}.txt'), 'w', encoding='utf8') as f:
    texts = []
    n_text = 0
    for line in tqdm(lines):
        n_line = len(line)
        texts.append(line)
        n_text += n_line
        if 4800 < n_text:
            for text in texts:
                text_area.send_keys(text)
                # time.sleep(1)
                
            time.sleep(5)
            translated = driver.find_element(by='id', value='txtTarget').text
            translated = translated.replace('.', '. ')
            f.write(translated)
            text_area.clear()
            
            texts = []
            n_text = 0
            
driver.quit()
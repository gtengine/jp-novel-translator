import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from save_novel import save_kakuyomu_novel, save_syosetu_novel
import time
from tqdm import tqdm

##################################################

def papago_translate(driver, title, novel_path, proportion):
    driver.maximize_window()
    driver.get('https://papago.naver.com/')
    time.sleep(2)
    
    text_area = driver.find_element(by='name', value='txtSource')
    text_area.send_keys(title)
    time.sleep(3)
    trans_title = driver.find_element(by='id', value='txtTarget').text
    driver.find_element(by='xpath', value='//*[@id="sourceEditArea"]/button').click()
    
    with open(novel_path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    
    n = int(len(lines) / proportion)
    length = 40
    for i in range(1, proportion + 1):
        txt = lines[n*(i-1) : n*i]
        if i == proportion:
            txt = lines[n*(proportion-1):]
        texts = []
        translated_texts = []
        rest = len(txt) % length
        final_idx = len(txt) - 1
        for idx, line in enumerate(tqdm(txt)):
            texts.append(line)
            if (len(texts) == length) or ((idx == final_idx) and (len(texts) == rest)):
                source = ''.join(texts)
                text_area.send_keys(source)
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/section/div/div[1]/div[2]/div/ul')))
                time.sleep(5)
                translated = driver.find_element(by='id', value='txtTarget').text
                translated = translated.replace('.', '. ')
                translated_texts.append(translated)
                driver.find_element(by='xpath', value='//*[@id="sourceEditArea"]/button').click()
                
                texts = []
            
        translated_path = novel_path.replace(title, f'{i}_{trans_title}')
        with open(translated_path, 'w', encoding='utf8') as f:
            for text in translated_texts:
                f.write(f'{text}\n\n')
    
    driver.quit()
    return translated_path



novel_url = 'https://kakuyomu.jp/works/1177354054882006371'
NOVEL_URL = "https://ncode.syosetu.com/n4936dp/"

# file_path, title = save_syosetu_novel(NOVEL_URL, os.getcwd())
# file_path = 'D:\\gitRepos\\jp-novel-translator\\転生貴族の異世界冒険録～自重を知らない神々の使徒～.txt'
# title = '転生貴族の異世界冒険録～自重を知らない神々の使徒～'

# file_path, title = save_kakuyomu_novel(novel_url, os.getcwd())
file_path = 'D:\\gitRepos\\jp-novel-translator\\女神様から同情された結果こうなった.txt'
title = '女神様から同情された結果こうなった'

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

file_path = papago_translate(driver, title, file_path, 3)
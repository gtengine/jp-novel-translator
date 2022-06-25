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

def papago_translate(title, novel_path, proportion, combine=False):
    options = Options()
    # options.add_argument('headless') # headless 모드 설정
    options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
    options.add_argument("disable-gpu") 
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    
    # 속도 향상을 위한 옵션 해제
    prefs = {
        'profile.default_content_setting_values': {
            'cookies' : 2,
            'images': 2,
            'plugins' : 2,
            'popups': 2,
            'geolocation': 2,
            'notifications' : 2,
            'auto_select_certificate': 2,
            'fullscreen' : 2,
            'mouselock' : 2,
            'mixed_script': 2,
            'media_stream' : 2,
            'media_stream_mic' : 2,
            'media_stream_camera': 2,
            'protocol_handlers' : 2,
            'ppapi_broker' : 2,
            'automatic_downloads': 2,
            'midi_sysex' : 2,
            'push_messaging' : 2,
            'ssl_cert_decisions': 2,
            'metro_switch_to_desktop' : 2,
            'protected_media_identifier': 2,
            'app_banner': 2,
            'site_engagement' : 2,
            'durable_storage' : 2
            }
        }   
    options.add_experimental_option('prefs', prefs)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    with open(novel_path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        
    def feed_text(text):
        text_area = driver.find_element(by='id', value='txtSource')
        text_area.send_keys(text)
        
    n = int(len(lines) / proportion)
    length = 30
    trans_title = ""
    path_list = []
    for i in range(0, proportion):
        txt = lines[n*i : n*(i+1)]
        if i == (proportion - 1):
            txt = lines[n*(proportion-1):]
            
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
        driver.get('https://papago.naver.com/')
        driver.implicitly_wait(10)
        
        if len(trans_title) == 0:
            feed_text(title)
            time.sleep(3)
            trans_title = driver.find_element(by='id', value='txtTarget').text
            trans_title = trans_title.replace(" ", "_").replace("?", "-")
            driver.find_element(by='xpath', value='//*[@id="sourceEditArea"]/button').click()
        
        texts = []
        translated_texts = []
        rest = len(txt) % length
        final_idx = len(txt) - 1
        for idx, line in enumerate(tqdm(txt)):
            texts.append(line)
            if (len(texts) == length) or ((idx == final_idx) and (len(texts) == rest)):
                source = ''.join(texts)
                feed_text(source)
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
                
        print(translated_path, "생성 완료.")
        path_list.append(translated_path)
        
        driver.quit()
        time.sleep(5)
        
    if combine:
        translated_path = novel_path.replace(title, f'[full]_{trans_title}')
        with open(translated_path, 'w', encoding='utf8') as new:
            for path in path_list:
                with open(path, 'r', encoding='utf8') as old:
                    for line in old:
                        new.write(line)
                print(path, "추가 완료.")
        print("파일 통합 완료.")
    
    return translated_path



# novel_url = 'https://kakuyomu.jp/works/1177354054884195461'
# file_path, title = save_kakuyomu_novel(novel_url, os.getcwd())
file_path, title = 'D:\gitRepos\jp-novel-translator\公女殿下の家庭教師.txt', '公女殿下の家庭教師'
file_path = papago_translate(title, file_path, 50, False)

# novel_url = "https://ncode.syosetu.com/n5409hr/"
# file_path, title = save_syosetu_novel(novel_url, os.getcwd())
# file_path = papago_translate(title, file_path, 50, True)
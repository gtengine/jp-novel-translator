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
    options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    options.add_argument("disable-gpu")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    def devide_list(lst, n_of_list):
        """원하는 수로 리스트 분할"""
        n = len(lst) // n_of_list
        re_l = [lst[i : i + n] for i in range(0, len(lst), n)]
        if len(re_l[-1]) < 100:
            for j in re_l[-1]:
                re_l[-2].append(j)
        return re_l[:-1]

    with open(novel_path, "r", encoding="utf8") as f:
        lines = f.readlines()
    devied_lines = devide_list(lines, proportion)

    def find_leng(lst_length):
        """한 번에 번역할 문장 수 설정"""
        n = 20
        while 20 <= n:
            if (lst_length % n) > (n * 0.8):
                break
            else:
                n = n + 1
        rest = lst_length % n
        return n, rest

    def feed_text(text):
        text_area = driver.find_element(by="id", value="txtSource")
        text_area.send_keys(text)

    trans_title = ""
    for i, l in enumerate(devied_lines):
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        driver.maximize_window()
        driver.get("https://papago.naver.com/")
        driver.implicitly_wait(10)

        if len(trans_title) == 0:
            feed_text(title)
            time.sleep(3)
            trans_title = driver.find_element(by="id", value="txtTarget").text
            trans_title = trans_title.replace(" ", "_").replace("?", "-")
            driver.find_element(
                by="xpath", value='//*[@id="sourceEditArea"]/button'
            ).click()

        length, rest = find_leng(len(l))
        texts = []
        translated_texts = []
        for idx, line in enumerate(tqdm(l)):
            texts.append(line)
            if (len(texts) == length) or (
                (idx == (len(l) - 1)) and (len(texts) == rest)
            ):
                source = " ".join(texts)
                feed_text(source)
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="root"]/div/div[1]/section/div/div[1]/div[2]/div/ul',
                        )
                    )
                )
                time.sleep(5)
                translated = driver.find_element(by="id", value="txtTarget").text
                translated = translated.replace(".", ". ")
                translated_texts.append(translated)
                driver.find_element(
                    by="xpath", value='//*[@id="sourceEditArea"]/button'
                ).click()
                texts = []

        translated_path = novel_path.replace(title, f"{i}_{trans_title}")
        with open(translated_path, "w", encoding="utf8") as f:
            for text in translated_texts:
                f.write(f"{text}\n\n")

        print(translated_path, "생성 완료.")

        driver.quit()

    if combine:
        # trans_title = ''
        print()
        print("=====" * 10)
        dir_path = os.path.join(os.getcwd(), "novel")
        file_list = os.listdir(dir_path)
        c = 0
        f_path_list = []
        while True:
            for file in file_list:
                try:
                    n = int(file.split("_")[0])
                    if c == n and trans_title in file:
                        f_path = os.path.join(dir_path, file)
                        f_path_list.append(f_path)
                except:
                    pass
            c += 1
            if c == len(file_list):
                break

        final_file = novel_path.replace(title, f"[full]_{trans_title}")
        with open(final_file, "w", encoding="utf-8") as ff:
            for f in f_path_list:
                with open(f, "r", encoding="utf-8") as ef:
                    for line in ef:
                        ff.write(line)
                print(f"추가 완료: {f}")
            print(f"\n파일 통합 완료: {final_file}")

    return final_file


novel_url = 'https://kakuyomu.jp/works/1177354054884195461'
file_path, title = save_kakuyomu_novel(novel_url, os.getcwd())
# novel_url = "https://ncode.syosetu.com/n3842hk/"
# file_path, title = save_syosetu_novel(novel_url, os.path.join(os.getcwd(), "novel"))

file_path = papago_translate(title, file_path, 10, True)

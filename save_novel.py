import os
import requests
from bs4 import BeautifulSoup

from tqdm import tqdm

##################################################

def save_syosetu_novel(base_url, novel_url, save_path):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"}

    res = requests.get(novel_url, headers=headers)
    if res.status_code == requests.codes.ok:
        print("사이트 접속 완료")
    else:
        print(f"사이트 접속 불가: [에러 코드: {res.status_code}]")
        
    soup = BeautifulSoup(res.text, 'html.parser')

    title = soup.find('p', attrs={'class':'novel_title'}).text
    description = soup.find('div', attrs={'id': 'novel_ex'}).text
    episodes = soup.find_all('dl', attrs={'class': 'novel_sublist2'})

    file_path = os.path.join(save_path, f"{title}.txt")
    name_map = dict()
    with open(file_path, 'w', encoding='utf8') as f:
        f.write(f'{title}\n\n')
        f.write(f'{description}\n')
        print("다운로드 중...")
        for episode in tqdm(episodes):
            chapter = episode.previous_sibling.previous_sibling
            if chapter['class'] == ['chapter_title']:
                f.write(f"{chapter.text}\n\n")
                
            link = f"{base_url}{episode.find('a')['href']}"
            resp = requests.get(link, headers=headers)
            ep_soup = BeautifulSoup(resp.text, 'html.parser')
            
            ep_title = ep_soup.find('p', attrs={'class': 'novel_subtitle'}).text
            f.write(f'{ep_title}\n\n')
            
            contents = ep_soup.find('div', attrs={'id': 'novel_honbun'})
            lines = contents.find_all('p')
            for line in lines:
                sentence = line.text.replace('「', ' " ').replace('」', ' " ').replace('『', ' " ').replace('』', ' " ')
                f.write(f'{sentence}\n')
            try:
                ep_view = ep_soup.find('div', attrs={'id': 'novel_a'})
                if ep_view:
                    f.write("====================\n")
                    view_lines = ep_view.find_all('p')
                    for view_line in view_lines:
                        sentence = view_line.text.replace('「', ' " ').replace('」', ' " ').replace('『', ' " ').replace('』', ' " ')
                        f.write(f'{sentence}\n')
                else:
                    f.write('\n')
            except:
                pass
            
    print("====="*10, '\n')
    print("소설 스크래핑 완료.")
    
    return file_path
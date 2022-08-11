import os
from attr import attr
import requests
from bs4 import BeautifulSoup

from tqdm import tqdm

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
}
##################################################


def save_syosetu_novel(novel_url, save_path):
    base_url = "https://ncode.syosetu.com"
    res = requests.get(novel_url, headers=headers)
    if res.status_code == requests.codes.ok:
        print("사이트 접속 완료")
    else:
        print(f"사이트 접속 불가: [에러 코드: {res.status_code}]")

    soup = BeautifulSoup(res.text, "html.parser")

    texts = []
    title = soup.find("p", attrs={"class": "novel_title"}).text
    texts.append(f"{title}\n\n")

    file_path = os.path.join(save_path, f"{title}.txt")
    if os.path.exists(file_path):
        print(file_path)
    else:
        description = soup.find("div", attrs={"id": "novel_ex"}).text
        texts.append(f"{description}\n\n")

        episodes = soup.find_all("dl", attrs={"class": "novel_sublist2"})
        print("=====" * 10)
        print("스크래핑 중...", "\n")
        for episode in tqdm(episodes):
            try:
                chapter = episode.previous_sibling.previous_sibling
                if chapter["class"] == ["chapter_title"]:
                    texts.append(f"{chapter.text}\n\n")
            except TypeError:
                pass

            link = f"{base_url}{episode.find('a')['href']}"
            resp = requests.get(link, headers=headers)
            ep_soup = BeautifulSoup(resp.text, "html.parser")

            ep_title = ep_soup.find("p", attrs={"class": "novel_subtitle"}).text
            texts.append(f"{ep_title}\n\n")

            contents = ep_soup.find("div", attrs={"id": "novel_honbun"})
            lines = contents.find_all("p")
            for line in lines:
                new_line = (
                    line.text.replace("「", '"')
                    .replace("」", '"')
                    .replace("『", '"')
                    .replace("』", '"')
                )
                if line.find("ruby"):
                    new_line = new_line.replace(
                        line.find("rb").text,
                        f"{line.find('rb').text}({line.find('rt').text})",
                    )
                texts.append(f"{new_line}\n")
            try:
                ep_view = ep_soup.find("div", attrs={"id": "novel_a"})
                if ep_view:
                    texts.append("====================\n")
                    view_lines = ep_view.find_all("p")
                    for view_line in view_lines:
                        new_view_line = (
                            view_line.replace("「", '"')
                            .replace("」", '"')
                            .replace("『", '"')
                            .replace("』", '"')
                        )
                        texts.append(f"{new_view_line}\n")
                else:
                    texts.append("\n")
            except:
                pass

        print("스크래핑 완료.", "\n")
        print("=====" * 10)
        print("파일 생성 중...", "\n")
        with open(file_path, "w", encoding="utf8") as f:
            for idx, text in enumerate(tqdm(texts)):
                texts[idx] = text.replace("\u3000", " ")
                f.write(texts[idx])

        print("파일 생성 완료.")

    return file_path, title


def save_kakuyomu_novel(novel_url, save_path):
    base_url = "https://kakuyomu.jp"
    res = requests.get(novel_url, headers=headers)
    if res.status_code == requests.codes.ok:
        print("사이트 접속 완료.")
    else:
        print(f"사이트 접속 불가: [에러 코드: {res.status_code}]")

    soup = BeautifulSoup(res.text, "html.parser")

    texts = []
    title = soup.find("h1", attrs={"id": "workTitle"}).text
    texts.append(f"{title}\n\n")

    file_path = os.path.join(save_path, f"{title}.txt")
    if os.path.exists(file_path):
        print(file_path)
    else:
        description = soup.find("p", attrs={"id": "introduction"}).text
        texts.append(f"{description}\n\n")

        episodes = soup.find_all("li", attrs={"class": "widget-toc-episode"})
        print("=====" * 10)
        print("스크래핑 중...", "\n")
        for episode in tqdm(episodes):
            try:
                chapter = episode.previous_sibling.previous_sibling
                if "widget-toc-chapter" in chapter["class"]:
                    texts.append(f"{chapter.text}\n\n")
            except TypeError:
                pass

            link = f"{base_url}{episode.find('a')['href']}"
            resp = requests.get(link, headers=headers)
            ep_soup = BeautifulSoup(resp.text, "html.parser")

            ep_header = ep_soup.find("header", attrs={"id": "contentMain-header"})
            ep_title = ep_header.find_all("p")[-1].text
            texts.append(f"{ep_title}\n\n")

            contents = ep_soup.find("div", attrs={"class": "widget-episode-inner"})
            lines = contents.find_all("p")
            for line in lines:
                new_line = (
                    line.text.replace("「", '"')
                    .replace("」", '"')
                    .replace("・", "-")
                    .replace("『", '"')
                    .replace("』", '"')
                )
                texts.append(f"{new_line}\n")
            texts.append(f"{'====='*4}\n")

        print("스크래핑 완료.", "\n")
        print("=====" * 10)
        print("파일 생성 중...", "\n")

        with open(file_path, "w", encoding="utf8") as f:
            for idx, text in enumerate(tqdm(texts)):
                texts[idx] = text.replace("\u3000", " ")
                f.write(texts[idx])

        print("파일 생성 완료.")

    return file_path, title

import requests
from bs4 import BeautifulSoup
import re

request_verification_token = ""
url = "https://www.wuxiaworld.com/account/login"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
                "referer": "https://www.wuxiaworld.com/"}
values = {"Email": "<TODO_EMAIL>", 
                "Password": "<TODO_PASSWORD>",
                "__RequestVerificationToken": request_verification_token,
                "RememberMe": "false"}

def is_new_chapter(chapter_id):
        chapter_id = str(chapter_id).strip()

        with requests.Session() as login:
            soup = BeautifulSoup(login.get(url).content, 'html.parser')
            request_verification_token = soup.find("input", attrs={"name":"__RequestVerificationToken"}).get("value")
            values["__RequestVerificationToken"] = request_verification_token
            login.post(url, data=values, headers=headers, allow_redirects=True)

            soup = BeautifulSoup(login.get("https://www.wuxiaworld.com/sponsored/overgeared/og-chapter-"+chapter_id).content, 'html.parser')
            get_chapter_header = "".join(map(str,soup.find_all("h4"))).lower() 
            if ("teaser" in get_chapter_header) and ("chapter" in get_chapter_header):
                return False
            else:
                return True


def parse_chapter(chapter_id):

        content = []
        chapter_id = str(chapter_id).strip()

        with requests.Session() as login:
            soup = BeautifulSoup(login.get(url).content, 'html.parser')
            request_verification_token = soup.find("input", attrs={"name":"__RequestVerificationToken"}).get("value")
            values["__RequestVerificationToken"] = request_verification_token
            login.post(url, data=values, headers=headers, allow_redirects=True)
            soup = BeautifulSoup(login.get("https://www.wuxiaworld.com/sponsored/overgeared/og-chapter-"+chapter_id).content, 'html.parser')
            get_chapter_header = soup.find("title").text
            content.append(get_chapter_header + "\n\n")
            html = soup.find_all('span', style=re.compile("vertical-align: baseline") )
            [ content.append(span.text + "\n") for span in html ]
            return content
            

if __name__ == "__main__":
    print(parse_chapter(str(1174)))

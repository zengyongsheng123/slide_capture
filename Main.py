'''
@File:Main.py
@Autho:南宫啸天
@Date:2025/6/3 23:22 
'''
import requests


headers = {
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Referer": "https://turing.captcha.gtimg.com/",
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Storage-Access": "active",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
    "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Microsoft Edge\";v=\"134\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
url = "https://turing.captcha.qcloud.com/cap_union_new_getcapbysig"
params = {
    "img_index": "1",
    "image": "0279050000747219000000098d20e17d4118",
    "sess": "s0jbKLCxqyMudh1wyo9NDfdDf7xN8nwmKMtyTMN7U0zBAbicIcbL5kfYL77yfutarYmdrp99CDkc2FBDld1oND5OdI-U4qprc5sId6N-lO1N0Orc8b3HCou4VfpHFdZBlZiXZK_yGscounemHEigBfN97UeUTJxxgPYFlvpgk_eTJhobYuvL0_laFpf3RARLTuZbeUe_NFgNc3d4OY7d6x3T541WajGixRlunt5bZzvVidFhSPJLyeMgzdF3COsEnn2CCEe1-TtLyuV4z4bw6dUZm6VBBXi18GIXXbK1YzRdK3pVaBIOFmuQ1dDinvvTN2GSyjUqtY-eEVJU4v4iCKMXYWIqI5KJlOV0h82JF-3m8Qr4PNh1ZtU8pHqyE1it-QZzBECkd1jGkYsM1emTsDoKkOFHYOojLyLMljlxJvMhg*"
}
response = requests.get(url, headers=headers, params=params)

with open("test9.png", "wb") as f:
    f.write(response.content)
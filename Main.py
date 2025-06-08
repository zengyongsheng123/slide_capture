import json
import re
import os
import requests
import time

headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Origin": "https://www.ishumei.com",
    "Referer": "https://www.ishumei.com/trial/captcha.html",
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

base_url = "https://captcha1.fengkongcloud.cn/ca/v1/register"
output_dir = "imgs"

# 创建目录
os.makedirs(output_dir, exist_ok=True)


def fetch_captcha_bg(captcha_uuid):
    """获取验证码背景图URL"""
    params = {
        "lang": "zh-cn",
        "rversion": "1.0.4",
        "data": "{}",
        "callback": f"sm_{int(time.time() * 1000)}",  # 动态生成callback
        "organization": "d6tpAY1oV0Kv5jRSgxQr",
        "sdkver": "1.1.3",
        "appId": "default",
        "model": "slide",
        "captchaUuid": captcha_uuid,  # 每次使用不同的UUID
        "channel": "DEFAULT"
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()

        # 提取JSON数据
        match = re.search(r'sm_\d+\((.*?)\)', response.text)
        if not match:
            return None

        json_data = json.loads(match.group(1))
        bg_url = "https://castatic.fengkongcloud.cn" + json_data["detail"]["bg"]
        return bg_url
    except Exception as e:
        print(f"请求失败: {e}")
        return None


def download_images(num_images=200):
    """下载指定数量的验证码图片"""
    for i in range(num_images):
        # 生成不同的captchaUuid（可以用时间戳+随机数）
        captcha_uuid = f"captcha_{int(time.time())}_{i}"

        bg_url = fetch_captcha_bg(captcha_uuid)
        if not bg_url:
            print(f"第 {i + 1} 张图片获取失败")
            continue

        try:
            img_data = requests.get(bg_url).content
            with open(f"{output_dir}/{i + 1}.jpg", "wb") as f:
                f.write(img_data)
            print(f"已下载第 {i + 1} 张图片: {bg_url}")
        except Exception as e:
            print(f"下载失败: {e}")

        time.sleep(1)  # 避免请求过快被封


if __name__ == "__main__":
    download_images(200)  # 下载200张不同的验证码图片

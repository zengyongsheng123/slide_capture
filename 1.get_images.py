import time
import uuid
import random
import os
import undetected_chromedriver as uc
import logging
from PIL import Image

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_uuid():
    """生成无横线的 UUID"""
    return str(uuid.uuid4()).replace('-', '')


def get_random_user_agent():
    """获取随机 User-Agent"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    ]
    return random.choice(user_agents)


def restart_browser():
    """重启浏览器并设置为全屏"""
    options = uc.ChromeOptions()
    options.add_argument('--window-size=1280,720')
    options.add_argument('--start-fullscreen')  # 启用全屏模式
    options.add_argument('--disable-blink-features=AutomationControlled')  # 隐藏自动化痕迹
    options.add_argument('--enable-javascript')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'user-agent={get_random_user_agent()}')

    # 强制匹配 Chrome 版本
    driver = uc.Chrome(version_main=136, options=options)
    logging.info("浏览器已初始化并设置为全屏模式")
    return driver


def main():
    # 创建输出目录
    output_dir = "./test_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 初始化浏览器
    driver = restart_browser()

    num = 0
    while True:
        try:
            # 访问目标网页
            logging.info("访问页面: https://dun.163.com/trial/jigsaw")
            driver.get('https://dun.163.com/trial/jigsaw')
            time.sleep(random.uniform(3, 5))  # 增加初始加载延迟

            # 点击“弹出式”按钮
            logging.info("寻找并点击‘弹出式’按钮")
            experience_btn = driver.find_element('xpath',
                                                 '//li[contains(text(), "弹出式") or contains(@class, "tcapt-tabs__tab active")]')
            driver.execute_script("arguments[0].scrollIntoView(true);", experience_btn)
            experience_btn.click()
            time.sleep(random.uniform(1, 2))  # 随机延迟

            # 点击“点击查看自定义样式”按钮
            logging.info("寻找并点击‘点击查看自定义样式’按钮")
            online_experience_btn = driver.find_element('xpath',
                                                        '//a[contains(text(), "点击查看自定义样式") or contains(@class, "u-mdtitle_btn j-custom")]')
            driver.execute_script("arguments[0].scrollIntoView(true);", online_experience_btn)
            online_experience_btn.click()
            time.sleep(random.uniform(1, 2))  # 随机延迟

            # 点击“登录”按钮
            logging.info("寻找并点击登录按钮")
            login_btn = driver.find_element('xpath',
                                            '//button[contains(text(), "登录") or contains(@class, "tcapt-bind_btn tcapt-bind_btn--login j-pop")]')
            driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
            login_btn.click()
            time.sleep(random.uniform(3, 5))  # 增加延迟等待验证码

            # 模拟鼠标移动
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(random.uniform(1, 2))

            # 抓取验证码图片
            for i in range(5):
                logging.info(f"抓取图片数量：{num}")
                uuid_str = get_uuid()

                # 查找验证码容器
                captcha_container = driver.find_element('xpath', '//div[contains(@class, "yidun_modal__body")]')
                driver.execute_script("arguments[0].scrollIntoView(true);", captcha_container)
                time.sleep(1)

                # 确保验证码容器可见并有有效尺寸
                for _ in range(10):
                    size = captcha_container.size
                    if size['width'] > 0 and size['height'] > 0:
                        break
                    logging.info("等待验证码容器尺寸加载...")
                    time.sleep(1)
                    driver.execute_script(
                        """
                        arguments[0].style.display = 'block';
                        arguments[0].style.visibility = 'visible';
                        arguments[0].style.width = '320px';
                        arguments[0].style.height = '160px';
                        arguments[0].style.position = 'relative';
                        arguments[0].style.opacity = '1';
                        arguments[0].style.zIndex = '9999';
                        arguments[0].removeAttribute('hidden');
                        """,
                        captcha_container
                    )
                else:
                    raise Exception("验证码容器尺寸无效")

                # 记录元素状态
                logging.info(f"CAPTCHA container size: {captcha_container.size}")
                location = captcha_container.location
                logging.info(f"CAPTCHA container location: {location}")

                # 等待验证码图片加载
                img_element = driver.find_element('xpath', '//img[contains(@class, "yidun_bg-img")]')
                for _ in range(10):
                    src = img_element.get_attribute('src')
                    if src and 'data:' not in src and img_element.is_displayed():
                        try:
                            driver.execute_script(
                                """
                                var img = arguments[0];
                                if (!img.complete || img.naturalWidth === 0) {
                                    throw new Error('Image not fully loaded');
                                }
                                """,
                                img_element
                            )
                            break
                        except:
                            logging.info("等待 CAPTCHA 图片加载...")
                            time.sleep(1)
                    else:
                        logging.info("等待 CAPTCHA 图片加载...")
                        time.sleep(1)
                else:
                    logging.warning("CAPTCHA 图片未加载完成")

                # 重试截图
                for attempt in range(3):
                    try:
                        captcha_container.screenshot(f"{output_dir}/{uuid_str}.png")
                        logging.info(f"验证码图片已保存至: {os.path.abspath(f'{output_dir}/{uuid_str}.png')}")
                        break
                    except Exception as e:
                        logging.warning(f"截图尝试 {attempt + 1} 失败: {e}")
                        time.sleep(2)
                        driver.execute_script(
                            """
                            arguments[0].style.width = '320px';
                            arguments[0].style.height = '160px';
                            """,
                            captcha_container
                        )
                else:
                    # 备用方案：全页面截图并裁剪
                    logging.info("多次尝试失败，尝试全页面截图")
                    driver.save_screenshot(f"{output_dir}/{uuid_str}_full.png")
                    logging.info(f"全页面截图已保存至: {os.path.abspath(f'{output_dir}/{uuid_str}_full.png')}")

                    if size['width'] > 0 and size['height'] > 0:
                        img = Image.open(f"{output_dir}/{uuid_str}_full.png")
                        crop_area = (
                            location['x'], location['y'],
                            location['x'] + size['width'], location['y'] + size['height']
                        )
                        cropped_img = img.crop(crop_area)
                        cropped_path = f"{output_dir}/{uuid_str}_cropped.png"
                        cropped_img.save(cropped_path)
                        logging.info(f"裁剪后的验证码图片已保存至: {os.path.abspath(cropped_path)}")
                    else:
                        logging.warning("无法裁剪：CAPTCHA 容器尺寸无效")

                # 点击刷新滑块
                slider = driver.find_element('xpath', '//button[contains(@class, "yidun_refresh")]')
                driver.execute_script("arguments[0].scrollIntoView(true);", slider)
                slider.click()
                time.sleep(random.uniform(1, 2))

                num += 1

            # 刷新页面
            logging.info("刷新页面")
            driver.refresh()
            time.sleep(random.uniform(2, 4))

        except Exception as e:
            logging.error(f"错误: {e}")
            error_screenshot_path = f"{output_dir}/error_{get_uuid()}.png"
            driver.save_screenshot(error_screenshot_path)
            logging.info(f"错误截图已保存至: {os.path.abspath(error_screenshot_path)}")
            if 'captcha_container' in locals():
                styles = driver.execute_script(
                    """
                    var el = arguments[0];
                    var styles = window.getComputedStyle(el);
                    return {
                        display: styles.display,
                        visibility: styles.visibility,
                        width: styles.width,
                        height: styles.height,
                        opacity: styles.opacity
                    };
                    """,
                    captcha_container
                )
                logging.info(f"CAPTCHA container computed styles: {styles}")
            with open('page.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            logging.info("页面HTML已保存至 page.html")
            driver.quit()
            driver = restart_browser()
            continue


if __name__ == "__main__":
    driver = None
    try:
        driver = main()  # 接收返回的 driver
    except KeyboardInterrupt:
        logging.info("程序被用户中断")
    finally:
        if driver is not None:
            driver.quit()


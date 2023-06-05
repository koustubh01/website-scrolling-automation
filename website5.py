from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from tempfile import mkdtemp
import boto3
import os

def handler(event,context):
    Options()
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome("/opt/chromedriver", options=options)
    website = event['website']
    duration = event['duration']
    crf = event['crf']
    speed = event['speed']
    #driver.get('https://stackoverflow.com/questions/1387997/how-can-i-retrieve-difference-between-two-columns-in-time-format')

    driver.get(website)

    # get window size
    s = driver.get_window_size()
    # obtain browser height and width
    w = driver.execute_script('return document.body.parentNode.scrollWidth')
    h = driver.execute_script('return document.body.parentNode.scrollHeight')
    print(w, h)
    h = min(5000, h)
    # set to new window size
    driver.set_window_size(w, h)
    # print(S)
    # driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment
    driver.find_element(By.TAG_NAME, 'body').screenshot('/tmp/web_screenshot.png')
    driver.set_window_size(s['width'], s['height'])
    driver.quit()
    s3=boto3.client('s3')
    s3.upload_file('/tmp/web_screenshot.png', 'website-scrolling-test', 'web_screenshot.png')

    #cmd = '/var/task/ffmpeg-6.0-amd64-static/ffmpeg -y -f lavfi -i color=s=1920x1080 -loop 1 -i "/tmp/web_screenshot.png" -filter_complex "[1:v]scale=1920:-2[fg]; [0:v][fg]overlay=y=-"t*h*0.04"[v]" -map "[v]" -speed 8 -t 9 "/tmp/output.mp4"'

    cmd = f'/var/task/ffmpeg-6.0-amd64-static/ffmpeg -loop 1 -i "/tmp/web_screenshot.png" -vf "scroll=vertical={speed},crop=iw:600:0:0,format=yuv420p" -preset superfast -crf {crf} -t {duration} -y "/tmp/output.mp4"'

    os.system(cmd)
    s3.upload_file('/tmp/output.mp4', 'website-scrolling-test', 'output.mp4')

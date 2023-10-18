import json
import os
import re
import subprocess
import time

import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "referer": "https://message.bilibili.com/"
}

def send_request(url):
    response = requests.get(url=url, headers=headers)
    return response

def get_video_data(html_data):
    title = re.findall('<title data-vue-meta="true">(.*?)</title>',html_data)[0].replace("_哔哩哔哩 (゜-゜)つロ 干杯~-bilibili","")
    json_data = re.findall(r'<script>window.__playinfo__=(.*?)</script>',html_data)[0]
    json_data = json.loads(json_data)
    #audio_url = json_data["data"]["dash"]["audio"][0]["backupUrl"][0]
    audio_url = json_data["data"]["dash"]["audio"][0]["baseUrl"]
    video_url = json_data["data"]["dash"]["video"][0]["baseUrl"]
    video_data = [title, audio_url, video_url]
    # print(video_data)
    return video_data

def save_data(file_name,audio_url,video_url):
    audio_data = send_request(audio_url).content#音频
    video_data = send_request(video_url).content#视频
    with open(file_name + ".mp3", "wb") as f:
        f.write(audio_data)
    with open(file_name + ".mp4", "wb") as f:
        f.write(video_data)

def merge_data(mkname,video_name,video_id=""):
    os.rename(video_name + ".mp3","1.mp3")
    os.rename(video_name + ".mp4","1.mp4")
    video_name = str(video_name).replace(' ','')#删除所有空格
    video_name = str(video_id)+'-'+video_name #添加视频编号排序
    cmd = "ffmpeg -i 1.mp4 -i 1.mp3 -acodec copy -vcodec copy "+ mkname+"/"+str(video_name) +".mp4"
    subprocess.Popen(cmd,shell=True,stderr=subprocess.DEVNULL)
    time.sleep(0.5)
    os.remove("1.mp3")
    os.remove("1.mp4")
    print(video_name)
    time.sleep(1)

def main():
    bilibili_bv = "BV18m4y1m7d9"  #视频bv号
    page_all = 1000               #选集才有页数
    mkdir_name = '下载视频'
    if not os.path.isdir(mkdir_name):
        os.mkdir(mkdir_name)
    for page_now in range(1000,page_all+1):
        url = "https://www.bilibili.com/video/"+bilibili_bv#+"?p="+str(page_now)
        html_data = send_request(url).text
        video_data = get_video_data(html_data)
        save_data(video_data[0],video_data[1],video_data[2])
        merge_data(mkdir_name,video_data[0],page_now)
if __name__ == "__main__":
    main()
'''

签到，评论任务

export zmh="xxxxxxx@xxxxxxx"

定时每天一次即可

cron: 0 0 10 * * *
const $ = new Env("致美化签到");

'''

import requests
import re
import json
import datetime
import os
import time
import random
from notify import send #导入青龙消息通知模块


def is_single_character_string(text):
    return isinstance(text, str) and len(text) == 1

#致美化执行
def zmh_xc():
    # 读取环境变量的账号和密码 @符号分割
    zmh = os.getenv('zmh')

    if '@' in zmh:
        # 账号格式正确
        zmh = zmh.split('@')
        zmh_zh = zmh[0]
        zmh_mm = zmh[1]
    else:
        # 账号格式不正确
        print('账号格式不正确 如：账号@密码')
        return

    # 获取初始token
    token_url = "https://zhutix.com/wp-json/b2/v1/getRecaptcha"
    token_data = {"number": "4", "width": "186", "height": "50"}
    token_head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://zhutix.com",
        "Referer": "https://zhutix.com/"}
    token_json = json.loads(requests.post(url=token_url, data=token_data, headers=token_head).text)
    # 登录致美化 获取登录token
    login_url = "https://zhutix.com/wp-json/jwt-auth/v1/token"
    login_data = {
        "nickname": "",
        "username": zmh_zh,
        "password": zmh_mm,
        "code": "",
        "img_code": "",
        "invitation_code": "",
        "token": token_json['token'],
        "smsToken": "",
        "luoToken": "",
        "confirmPassword": "",
        "loginType": ""}
    login_head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://zhutix.com",
        "Referer": "https://zhutix.com/"}
    login_resp = requests.post(url=login_url, data=login_data, headers=login_head)
    login_json = json.loads(login_resp.text)
    if login_json['id'] != "":
        token = login_json['token']
        name = login_json['name']
        returnsLogs = name + " 登录成功 开始签到"
        print(returnsLogs)

        #执行签到任务 >>>>>>
        sign_url = "https://zhutix.com/wp-json/b2/v1/userMission"
        sign_head = {
                    "Authorization": "Bearer " + token,
                    "Host": "zhutix.com",
                    "Origin": "https://zhutix.com",
                    "Referer": "https://zhutix.com/mission/today",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
        sign_resp = requests.post(url=sign_url,headers=sign_head)
        sign_json = json.loads(sign_resp.text)
        if is_single_character_string(sign_resp.text) == True:
            returnsLogs = returnsLogs + "\n" + "签到时间：" + sign_json['mission']['date']
            returnsLogs = returnsLogs + "\n" + "获得奖励：" + sign_json['mission']['credit']
            print("签到时间：" + sign_json['mission']['date'])
            print("获得奖励：" + sign_json['mission']['credit'])
        else:
            returnsLogs = returnsLogs + "\n" + "签到失败：今日已签到 签到获取：" + sign_resp.text
            print("签到失败：今日已签到 签到获取：" + sign_resp.text)
    else:
        print("登录失败 请检查账号或密码")
        eturnsLogs = "登录失败 请检查账号或密码"

    #执行评论任务
    for i in range(3):
        newPost_resp = requests.get(url="https://zhutix.com/pc/page/" + str(random.randint(1, 37)) + "/")
        newPost_list = re.findall('<a href="(.*?)" class="imglist-char shu" target="_blank">(.*?)</a>',newPost_resp.text)
        # print(newPost_list[0][0])
        serialNumber = random.randint(1,24)
        newPost_url = newPost_list[int(serialNumber)][0]
        string = requests.get(url=newPost_url)
        string.encoding = string.apparent_encoding

        #获取网站id
        web_id = re.findall('"language":"zh_CN","post_id":"(.*?)","author_id":"(.*?)","poster_box":"<',string.text)
        id = web_id[0][0]
        comments_url = "https://zhutix.com/wp-json/b2/v1/commentSubmit"
        comments_data = {
            "comment_post_ID": id,
            "author": name,
            "comment": "支持一下！",
            "comment_parent": "0",
            "img[imgUrl]": "",
            "img[imgId]": ""}
        comments_head = {
            "Authorization": "Bearer " + token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Origin": "https://zhutix.com",
            "Referer": newPost_url}
        comments_resp = requests.post(url=comments_url, data=comments_data, headers=comments_head)
        print(newPost_list[int(serialNumber)][1] + ' 评论成功 延迟60秒')
        if i <3 :
            returnsLogs = returnsLogs + "\n" + newPost_list[serialNumber][1] + ' 评论成功 延迟60秒'
            time.sleep(60)

    # 执行完成 发送通知
    send('致美化签到', returnsLogs + '\n\n本通知 By github https://github.com/TOMhongshu/-qiandao/ \n通知时间:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    zmh_xc()

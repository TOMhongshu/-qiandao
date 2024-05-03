'''

每日签到，自动完成评论任务

export zmh="xxxxxxx@xxxxxxx"

每天执行一次即可

cron: 0 0 10 * * *
const $ = new Env("致美化签到");
'''

import requests
import json
import os
import re
import time
import random
import logging
import datetime
from notify import send #导入青龙消息通知模块

def is_single_character_string(text):
    return isinstance(text, str) and len(text) == 1

def zmh_xc():
    # 分割账号
    zmh = os.getenv('zmh')

    if '@' in zmh:
        # 账号格式正确
        zmh = zmh.split('@')
        zmh_zh = zmh[0]
        zmh_mm = zmh[1]
    else:
        # 账号格式不正确
        returnsLogs = '账号格式不正确 如：账号@密码'
        print('账号格式不正确 如：账号@密码')

    # 关闭证书报错
    requests.packages.urllib3.disable_warnings()

    # 获取token
    get_url = 'https://zhutix.com/wp-json/b2/v1/getRecaptcha'
    get_data = {"number": "4", "width": "186", "height": "50"}
    get_head = {
        "Origin": "https://zhutix.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        "Referer": "https://zhutix.com/"}
    get_resp = requests.post(url=get_url, data=get_data, headers=get_head, stream=True, verify=False).json()
    token = get_resp['token']

    # 执行登录操作
    print('开始登录>>>')
    returnsLogs = '开始登录>>>'
    login_url = 'https://zhutix.com/wp-json/jwt-auth/v1/token'
    login_data = params = {
        "nickname": "",
        "username": zmh_zh,
        "password": zmh_mm,
        "code": "",
        "img_code": "",
        "invitation_code": "",
        "token": token,
        "smsToken": "",
        "luoToken": "",
        "confirmPassword": "",
        "loginType": ""}
    login_head = {
        "Origin": "https://zhutix.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        "Referer": "https://zhutix.com/"}
    login_resp = requests.post(url=login_url, data=login_data, headers=login_head, stream=True, verify=False)
    login_resp.encoding = login_resp.apparent_encoding
    login_json = json.loads(login_resp.text)
    login_cookie = login_resp.cookies

    # 获取账号信息
    print('\n开始获取账号信息>>>')
    returnsLogs = returnsLogs + '\n' + '开始获取账号信息>>>'
    if login_json['id'] != "":
        name = login_json['name']  # 昵称
        credit = login_json['lv']['lv']['credit']  # 锋币
        lv_name = login_json['lv']['lv']['name']  # 等级名称
        lv_lv = login_json['lv']['lv']['lv']  # 等级
        token = login_json['token']  # 登录后token
        returnsLogs = returnsLogs + '\n' + '账号名称：' + name + '\n' + '当前锋币：' + str(
            credit) + '\n' + '当前等级：' + lv_name + lv_lv + '\n'
        print('账号名称：' + name + '\n' + '当前锋币：' + str(credit) + '\n' + '当前等级：' + lv_name + lv_lv + '\n')

        # 开始执行签到任务>>>
        print('\n开始执行签到任务>>>')
        returnsLogs = returnsLogs + '\n' + '开始执行签到任务>>>'
        sign_url = 'https://zhutix.com/wp-json/b2/v1/userMission'
        sign_head = {
            "Authorization": "Bearer " + token,
            "Origin": "https://zhutix.com",
            "Host": "zhutix.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
            "Referer": "https://zhutix.com/mission/today"}
        cookie = requests.utils.dict_from_cookiejar(login_cookie)
        sign_resp = requests.post(url=sign_url, data={}, headers=sign_head, cookies=cookie, stream=True, verify=False)
        sign_resp.encoding = sign_resp.apparent_encoding
        sign_json = json.loads(sign_resp.text)
        if is_single_character_string(sign_resp.text) == True:
            print("签到时间：" + sign_json['mission']['date'])
            print("获得奖励：" + sign_json['mission']['credit'])
            returnsLogs = returnsLogs + '\n' + "签到时间：" + sign_json['mission']['date']
            returnsLogs = returnsLogs + '\n' + "获得奖励：" + sign_json['mission']['credit']
        else:
            print("签到失败：今日已签到 签到获取：" + sign_resp.text + " 锋币")
            returnsLogs = returnsLogs + '\n' + "签到失败：今日已签到 签到获取：" + sign_resp.text + " 锋币"

        # 开始执行评论任务
        print('\n开始执行评论任务>>>')
        returnsLogs = returnsLogs + '\n' + "开始执行评论任务>>>"
        for i in range(3):
            newPost_resp = requests.get(url="https://zhutix.com/pc/page/" + str(random.randint(1, 37)) + "/",
                                        stream=True, verify=False)
            newPost_list = re.findall('<a href="(.*?)" class="imglist-char shu" target="_blank">(.*?)</a>',
                                      newPost_resp.text)
            # print(newPost_list[0][0])
            serialNumber = random.randint(1, 24)
            newPost_url = newPost_list[int(serialNumber)][0]
            string = requests.get(url=newPost_url, stream=True, verify=False)
            string.encoding = string.apparent_encoding

            # 获取网站id
            web_id = re.findall('"language":"zh_CN","post_id":"(.*?)","author_id":"(.*?)","poster_box":"<', string.text)
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
            comments_resp = requests.post(url=comments_url, data=comments_data, headers=comments_head, stream=True,
                                          verify=False)
            print(newPost_list[int(serialNumber)][1] + ' 评论成功 延迟60秒')
            if i < 3:
                returnsLogs = returnsLogs + "\n" + newPost_list[serialNumber][1] + ' 评论成功 延迟60秒'
                time.sleep(60)

            # 执行完成 发送通知
            send('致美化签到',returnsLogs + '\n\n本通知 By github https://github.com/TOMhongshu/-qiandao/ \n通知时间:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        print('登录失败')

if __name__ == "__main__":
    zmh_xc()

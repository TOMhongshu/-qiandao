'''

精易论坛签到脚本

export bbs125 = "cookie@formhash"

定时每天一次即可

cron: 0 0 10 * * *
const $ = new Env("精易论坛签到");

'''

import requests
import json
import datetime
import os
from notify import send #导入青龙消息通知模块

def jingyi():
    # 读取环境变量 @符号分割
    JYcookie = os.getenv('JY_cookie')

    # JYcookie = ""

    if '@' in JYcookie:
        # cookie格式正确
        JYcookie = JYcookie.split('@')
        JY_cookie = JYcookie[0]
        JY_formhash = JYcookie[1]
    else:
        print("cookie格式不正确 如cookie@formhash")
        return

    #签到
    sign_url = "https://bbs.125.la/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1"
    sign_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0", #可填可不填
                "cookie": JY_cookie, #必填
                "referer": "https://bbs.125.la/dsu_paulsign-sign.html"}
    sign_data = {
        "formhash": JY_formhash,
        "submit": "1",
        "targerurl": "",
        "todaysay": "",
        "qdxq": "kx"}
    sign_resp = requests.post(url=sign_url,data=sign_data,headers=sign_headers)
    sign_resp.encoding = sign_resp.apparent_encoding
    print(sign_resp.text)
    sign_json = json.loads(sign_resp.text)

    if sign_json["status"] == 1:
        returnsLogs = ""
        returnsLogs = returnsLogs + "\n" + "积累签到次数:", sign_json["data"]["days"]
        print("积累签到次数:", sign_json["data"]["days"])
        returnsLogs = returnsLogs + "\n" + "本月签到次数:", sign_json["data"]["mdays"]
        print("本月签到次数:", sign_json["data"]["mdays"])
        returnsLogs = returnsLogs + "\n" + "当前总有奖励:", sign_json["data"]["reward"]
        print("当前总有奖励:", sign_json["data"]["reward"])
        returnsLogs = returnsLogs + "\n" + "上一次签到是:", sign_json["data"]["qtime"]
        print("上一次签到是:", sign_json["data"]["qtime"])
    else:
        returnsLogs = sign_json["msg"]
        print(sign_json["msg"])

    # print('精易论坛签到', returnsLogs + '\n\n本通知 By github https://github.com/TOMhongshu/-qiandao/ \n通知时间:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 执行完成 发送通知
    send('精易论坛签到', returnsLogs + '\n\n本通知 By github https://github.com/TOMhongshu/-qiandao/ \n通知时间:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    jingyi()

/*

葫芦侠签到脚本

export hlx = "手机号@密码"

定时每天一次即可


cron: 0 0 8 * *
const $ = new Env("葫芦侠签到");

*/

import requests
import json
import datetime
import hashlib
import time
import os
from notify import send #导入青龙消息通知模块

#MD5加密
def md5_jm(param):
    m = hashlib.md5()
    b = param.encode(encoding='utf-8')
    m.update(b)
    passwd_md5 = m.hexdigest()
    return passwd_md5

def hlx():
    # 测试账号
    # hlx = ''

    # 读取环境变量 @符号分割
    hlx = os.getenv('hlx')

    if '@' in hlx:
        # 格式正确
        hlx = hlx.split('@')
        username = hlx[0]
        password = hlx[1]
    else:
        # 格式错误
        print("cookie格式不正确 如手机号@密码")
        return

    #登录获取账号key
    password = hashlib.md5(password.encode('utf-8')).hexdigest()

    #sign计算
    sign = "account" + username + "device_code[d]b305cc73-8db8-4a25-886f-e73c502b1e99password" + password + "voice_codefa1c28a5b62e79c3e63d9030b6142e4b"
    sign = hashlib.md5(sign.encode('utf-8')).hexdigest()

    #登录葫芦侠
    #设置提交地址
    login_url = "http://floor.huluxia.com/account/login/ANDROID/4.1.8?platform=2&gkey=000000&app_version=4.2.1.6.1&versioncode=367&market_id=tool_web&_key=&device_code=%5Bd%5Db305cc73-8db8-4a25-886f-e73c502b1e99&phone_brand_type=VO"
   #设置提交参数
    login_data = {'account': username, 'login_type': '2', 'password': password, 'sign': sign}
    #设置提交协议头
    login_head = {"User-Agent": "okhttp/3.8.1"}
    login_resp = requests.post(url=login_url, data=login_data, headers=login_head)
    login_resp.encoding = login_resp.apparent_encoding
    #json解析
    login_json = json.loads(login_resp.text)
    #提取key数据
    _key = login_json['_key']

    #葫芦侠签到
    print("============================开始签到请耐心等待============================")
    returnsLogs = ''
    returnsLogs = returnsLogs + "\n" + "============================开始签到请耐心等待============================"
    #初始化数据
    number = 0  # 成功计数
    continueDays = 0  # 连续签到天数
    experienceVal = 0  # 本次签到经验

    for i in range(1,125):
        #签到id
        cat_id = str(i)
        #获取时间戳
        timestamp = str(time.time()).split(".")[0] + str(time.time()).split(".")[1][0:3]
        #无需device_code版本
        signInURL = f"http://floor.huluxia.com/user/signin/ANDROID/4.1.8?platform=2&gkey=000000&app_version=4.2.0.5&versioncode=20141475&market_id=floor_web&_key={_key}&phone_brand_type=OP&cat_id={cat_id}&time={timestamp}"
        # 使用split方法按照'&'字符分割URL
        params = signInURL.split('&')
        # 遍历分割后的字符串列表，找到cat_id和time参数
        at_id1 = None
        time1 = None
        for param in params:
            if 'cat_id' in param:
                cat_id1 = param.split('=')[1]
            elif 'time' in param:
                time1 = param.split('=')[1]
        # 将cat_id和time和不变的voice_code组合成一个字符串
        sign = md5_jm('cat_id' + cat_id1 + 'time' + time1 + 'fa1c28a5b62e79c3e63d9030b6142e4b')
        signIndata = {"sign": sign }#动态sign
        signInhead = {
            "Accept-Encoding": "identity",
            "Host": "floor.huluxia.com",
            'User-Agent': 'okhttp/3.8.1',
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "37"}
        signInresp = requests.post(url=signInURL, data=signIndata, headers=signInhead)
        dic = signInresp.json()
        # 获取签到的状态，状态：0为失败，1为成功。
        status = dic['status']
        tt = "\t"
        if status == 1:
            continueDays = dic['continueDays']  # 连续签到天数
            experienceVal = dic['experienceVal']  # 本次签到经验
            number += 1  # 每次签到成功就+1，最后记总成功次数。
            msg = f'版块ID为{cat_id}{tt}签到状态：成功{tt}获得{experienceVal}点经验/已连签{continueDays}天{tt}第{number}次签到成功！'
            # print(msg)
        else:
            msg = f'版块ID为{cat_id}{tt}签到状态：失败{tt}你的_key已失效或此版块可能已经不存在！'
        print(msg)
        time.sleep(2)  # 稍做延时，太快会异常。
    # 获取结果：累计连续签到天数及本次签到共获得多少经验点数。
    print(f"\n签到结果：此账号已连续签到{continueDays}天，此次签到共成功获{experienceVal * number}点经验！继续加油哦！")
    returnsLogs = returnsLogs + f"\n签到结果：此账号已连续签到{continueDays}天，此次签到共成功获{experienceVal * number}点经验！继续加油哦！"

    # 执行完成 发送通知
    send('葫芦侠签到',returnsLogs + '\n\n本通知 By github https://github.com/TOMhongshu/-qiandao/ \n通知时间:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    hlx()

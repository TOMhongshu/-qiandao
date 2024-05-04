'''
菜鸟图库自动签到,定时每天一次即可
export cntk="手机号@密码"
cron: 0 0 10 * * *
const $ = new Env("菜鸟图库签到");
'''

import requests
import datetime
import os
import time
from notify import send #导入青龙消息通知模块

# 关闭证书报错
requests.packages.urllib3.disable_warnings()

def cntk_xc():
    returnsLogs = ''
    cntk = os.getenv('cntk')

    if '@' in cntk:
        # 账号格式正确
        cntk = cntk.split('@')
        cntk_zh = cntk[0]
        cntk_mm = cntk[1]
    else:
        # 账号格式不正确
        print('账号格式不正确 如：手机号@密码')
        returnsLogs = '账号格式不正确 如：手机号@密码'
        return

    login_url = 'https://www.sucai999.com/default/index/login?t=' + str(int(time.time() * 1000))
    login_data = {"username": cntk_zh, "password": cntk_mm, "type": "2"}
    login_resp = requests.post(login_url, data=login_data, verify=False)
    cookie = login_resp.cookies.get_dict()
    if login_resp.json()['code'] == 0:
        print("菜鸟图库登录成功 >>>\n")
        returnsLogs = "菜鸟图库登录成功 >>>\n"
        message_url = 'https://www.sucai999.com/default/index/get_userinfo'
        message_resp = requests.get(message_url, verify=False, cookies=cookie)
        print("开始获取用户信息 >>>\n")
        print('用户名称：' + message_resp.json()['nickname'])
        print('账户余额：' + message_resp.json()['balance'])
        print('用户图币：' + str(message_resp.json()['sucaibalance']))
        print('用户会员：' + message_resp.json()['birdhome'])
        print('用户时长：' + message_resp.json()['vip_time'])
        print('用户会员：' + message_resp.json()['birdhome'])
        print('作品数量：' + message_resp.json()['sucai_count'] + '\n\n')
        returnsLogs = returnsLogs + "开始获取用户信息 >>>\n" + '用户名称：' + message_resp.json()['nickname'] + '\n' + '账户余额：' + message_resp.json()['balance'] + '\n' + '用户图币：' + message_resp.json()['sucaibalance'] + '\n'+ '用户会员：' + message_resp.json()['birdhome'] + '\n' + '用户时长：' + message_resp.json()['vip_time'] + '\n' + '用户会员：' + message_resp.json()['birdhome'] + '\n' + '作品数量：' + message_resp.json()['sucai_count'] + '\n\n'
        sign_url = 'https://www.sucai999.com/default/qiandao/qd'
        sign_resp = requests.get(sign_url, verify=False, cookies=cookie)
        if sign_resp.json()['status'] == 1:
            print(sign_resp.json()['msg'] + '\n')
            print(sign_resp.json()['content'] + '\n')
            print(sign_resp.json()['yiqiandao'] + '\n')
            print('获得图币：' + sign_resp.json()['num'] + '\n')
            returnsLogs = returnsLogs + sign_resp.json()['msg'] + '\n' + sign_resp.json()['content'] + '\n' + sign_resp.json()['yiqiandao'] + '\n' + '获得图币：' + sign_resp.json()['num'] + '\n'
        else:
            returnsLogs = returnsLogs + sign_resp.json()['msg'] + '\n'
    else:
        print("菜鸟图库登录失败，请检查账号是否正确 >>>")
        returnsLogs = "菜鸟图库登录失败，请检查账号是否正确 >>>"
        return

    send('菜鸟图库签到', returnsLogs + '\n\n本通知 By github https://github.com/TOMhongshu/-qiandao/ \n通知时间:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    cntk_xc()

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import json

# 请自己填入自己的账号密码
account = 'xxxxxxxxxx'
passwd = 'xxxxxxxxxxx'

# 自定义的Headers
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                  'AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/67.0.3396.99 '
                  'Safari/537.36',
    'Host': "www.educoder.net",
    'Referer':'None',
    'Origin':'https://www.educoder.net',
    'Connection': 'keep-alive',
    'Sec-Fetch-Site':'same-origin',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Dest':'empty',
    'Accept':'application/json, text/plain, */*',
}

#账号密码信息
loginJson = {
    'login':account,
    'password':passwd,
    'autologin':1
}


randomPara = 'randomcode=1588733273&client_key=13d443fc3a3b45ad429312bbad2b2a6d' # 随机数参数
attendanceUrl = 'https://www.educoder.net/api/users/attendance.json?' + randomPara # 签到URL

# 获取Cookie和登录信息
eduUrl = 'https://www.educoder.net/api/accounts/login.json?' + randomPara

loginRes = requests.post(eduUrl, json=loginJson)
loginCookieDict = requests.utils.dict_from_cookiejar(loginRes.cookies)
loginResDict = json.loads(loginRes.text)
print(loginCookieDict)

for item in loginResDict:
    print(item+':'+str(loginResDict[item]))

# 获取必要信息
userId = loginResDict['user_id']
userLogin = loginResDict['login']
userName = loginResDict['name']
userGrade = loginResDict['grade']
userIdentity = loginResDict['identity']
userSchool = loginResDict['school']

homePage = 'https://www.educoder.net/api/users/' + userLogin + '/homepage_info.json?' + randomPara # 主页面的URL

# 签到
Referer = 'https://www.educoder.net/users/' + userLogin + '/classrooms' # 记录一下Referer，模拟的真一点
header['Referer'] = Referer
resAttend = requests.post(attendanceUrl, headers = header, cookies = loginCookieDict)
resHome = requests.get(homePage, headers = header, cookies = loginCookieDict)
attendanceResDict = json.loads(resAttend.text) # 签到后获得的响应，打包成字典
homePageInfoDict = json.loads(resHome.text) # 获取主页面的相应
def qiandao():
    print('尝试签到...')
    if attendanceResDict['status'] == 0:
        print(f'签到成功,当前{attendanceResDict["grade"]},下一级{attendanceResDict["next_gold"]}')
    else:
        print(f'已经签到过,当前经验{homePageInfoDict["experience"]},金币{homePageInfoDict["grade"]}')

def main_handler(event, context):
    qiandao()

if __name__ == '__main__':
    main_handler("", "")

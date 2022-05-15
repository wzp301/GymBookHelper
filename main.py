import time
# from bs4 import BeautifulSoup
import os
from util import *

class GymBookHelper:

    username = ""
    pwd = ""
    encode_pwd = ""
    authcode = ""
    key = ""
    request = None
    courtNum = 301
    webDataProcessor = None
    common_header = {
        'authority': 'gym.cqnu.edu.cn',
        'method': 'GET',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'csxrz.cqnu.edu.cn',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    def __init__(self, username, pwd):
        if username == "" or pwd == "":
            raise Exception("GymBookHelper Error! username or pwd is empty, Please input right username or pwd!")
        self.username = username
        self.pwd = pwd
        self.request = NetRequest()
        self.webDataProcessor = WebDataProcessor()

    def getVerCode(self):
        url = "https://csxrz.cqnu.edu.cn/cas/verCode?random=" + str(int(round(time.time() * 1000)))
        headers = self.common_header
        headers.update({
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        })
        res = self.request.get(url, header=headers)
        with open("res/verCode.jpg", 'wb') as f:
            f.write(res.content)
        self.authcode = self.webDataProcessor.getAuthcode("res/verCode.jpg")
        print("getVerCode----authcode = ", self.authcode)

    def getLoginPage(self):
        url = "https://csxrz.cqnu.edu.cn/cas/login?service=https://gym.cqnu.edu.cn/app/product/show.html?id=301"
        headers = self.common_header
        headers.update({
            'sec-fetch-dest': 'document',
        });
        res = self.request.get(url, header=headers)
        self.key = self.webDataProcessor.parseKeyFromHtml(res.text)
        self.encode_pwd = self.webDataProcessor.getEncodePwd(self.pwd, self.key)
        print(self.key)
        # 验证码识别出错重试
        self.getVerCode()
        while len(self.authcode) != 4:
            self.getVerCode()

    def getSessionId(self):
        url = "https://csxrz.cqnu.edu.cn/cas/login?service=https://gym.cqnu.edu.cn/app/product/show.html?id=301"
        headers = {
            'authority': 'gym.cqnu.edu.cn',
            'method': 'GET',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Host': 'csxrz.cqnu.edu.cn',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
        }
        self.request.get(url, header=headers)
        cookies = self.request.getCookies()
        if len(cookies) != 0:
            self.request.setSessionId(cookies[0][0] + "=" + cookies[0][1])
        else:
            raise Exception("GymBookHelper Error! %s login failure!" % (self.username))

    def login(self):
        # url = "https://csxrz.cqnu.edu.cn/cas/login;jsessionid={session_id}?service=https://gym.cqnu.edu.cn/app/product/show.html?id=301".format(session_id = self.request.getLoginBeforeSessionId())
        url = "https://csxrz.cqnu.edu.cn/cas/login?service=https://gym.cqnu.edu.cn/app/product/show.html?id=301"
        data = {
            'username': self.username,
            'password': self.encode_pwd,
            'authCode': self.authcode,
            'It': self.key,
            "execution": "e1s1",
            "_eventId": "submit",
            'isQrSubmit': 'false',
            'qrValue': '',
            'isMobileLogin': 'false'
        }
        headers = self.common_header
        headers.update({
            'method': 'POST',
            'scheme': 'https',
            'content-length': str(self.request.getContentLength(data)),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'contenttype': 'application/x-www-form-urlencoded',
            'origin': 'https://gym.cqnu.edu.cn',
            'referer': 'https://csxrz.cqnu.edu.cn/cas/login?service=https://gym.cqnu.edu.cn/app/product/show.html?id=301',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
        });
        # 发送登陆请求
        res = self.request.post(url, headers, data=data)
        with open("./res/login_res.html", 'w', encoding='utf-8') as f:
            f.write(res.text)
        print(res)
    def chooseTimeRange(self):
        url = "https://gym.cqnu.edu.cn/login.html?id=" + str(self.courtNum)
        headers = {
            'authority': 'gym.cqnu.edu.cn',
            'method': 'GET',
            'path': '/product/show.html?id=' + str(self.courtNum),
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cookie' : 'from=undefined; JSESSIONID=%s; errortime=0; from=undefined',
            'cache-control': 'max-age=0',
            'content-length': '60',
            'contenttype': 'application/x-www-form-urlencoded',
            'referer': 'https://gym.cqnu.edu.cn/product/productlist.html?code=100000',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
        self.request.get(url, headers)

# read user imformation from local file
def readUserInfoFromFile(filename):
    usersInfo = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            info = line.split(',')
            # print(info)
            user = {
                "name" : info[0],
                "pwd" : info[1]
            }
            usersInfo.append(user)
    return usersInfo

if __name__ == "__main__":
    # usersInfo = readUserInfoFromFile("./userInfo.txt")
    jbh = GymBookHelper("2021210516081", "084413")
    jbh.getLoginPage()
    jbh.login()
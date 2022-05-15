import requests
import time
import os
import ddddocr
from urllib.parse import urlencode
from pyDes import des, ECB, PAD_PKCS5
import base64
from bs4 import BeautifulSoup

class NetRequest:
    session = None
    sessionId = ""
    cookies_file = "cookies.txt"
    cookies_cache = None
    verFile = "./res/charles.pem"

    def __init__(self):
        self.session = requests.Session()  # create session

    def setSessionId(self, sid):
        self.sessionId = sid

    def getCookies(self):
        return self.session.cookies.items()

    def post(self, url, header, data):
        c_cookies = self.get_cookie_from_file()
        self.record_request(url, data, header, c_cookies)
        res = self.session.post(url, headers=header, data=data, verify=False)
        cookies = self.getCookies()  # 如果响应头中包含了Set-Cookie，则cookies不为空
        if len(cookies) > 0:
            self.cookies_cache = cookies[0][0] + "=" + cookies[0][1]
        print(self.cookies_cache)
        print("Post " + url + ", data = " + str(data) + "old_cookies = " + str(
            c_cookies) + ", new_cookies = {}" + "headers = " + str(header))
        # if len(cookies) != 0:
        #     old_cookie_set_len = len(self.cookies_set)
        #     self.save_cookie_to_file(cookies)
        #     new_cookie_set_len = len(self.cookies_set)
        #     if old_cookie_set_len != new_cookie_set_len:
        #         print("Post " + url + ", data = " + str(data) + "old_cookies = " + str(
        #             c_cookies) + ", new_cookies = " + str(cookies) + "headers = " + str(header))
        #     else:
        #         print(
        #             "Post " + url + ", data = " + str(data) + "old_cookies = " + str(c_cookies) + ", new_cookies = {}" + "headers = " + str(header))
        #
        # else:
        #     print("Post " + url + ", data = " + str(data) + "old_cookies = " + str(c_cookies) + ", new_cookies = {}" + "headers = " + str(header))
        return res

    def get(self, url, header):
        c_cookies = self.get_cookie_from_file()
        self.record_request(url, {}, header, c_cookies)
        res = self.session.get(url, headers=header, verify=False)
        cookies = self.getCookies()  # 如果响应头中包含了Set-Cookie，则cookies不为空
        if len(cookies) > 0:
            self.cookies_cache = cookies[0][0] + "=" + cookies[0][1]
        print(self.cookies_cache)
        print("Get " + url + "old_cookies = " + str(c_cookies) + ", new_cookies = " + str(cookies) + "headers = " + str(header))
        # if len(cookies) != 0:
        #     old_cookie_set_len = len(self.cookies_set)
        #     self.save_cookie_to_file(cookies)
        #     new_cookie_set_len = len(self.cookies_set)
        #     if old_cookie_set_len != new_cookie_set_len:
        #         print("Get " + url + "old_cookies = " + str(c_cookies) + ", new_cookies = " + str(cookies) + "headers = " + str(header))
        #     else:
        #         print("Get " + url + "old_cookies = " + str(c_cookies) + ", new_cookies = {}" + "headers = " + str(header))
        # else:
        #     print("Get " + url + "old_cookies = " + str(c_cookies) + ", new_cookies = {}" + "headers = " + str(header))
        return res

    def getLoginBeforeSessionId(self):
        return self.cookies_cache

    def save_cookie_to_file(self, cookies):
        pass
        # if len(cookies) == 1
        #     self.cookies_set.add(cookie[0] + "=" + cookie[1])
        # with open('cookies.txt', 'a') as f:
        #     for cookie in cookies:
        #         f.write(cookie[0] + "=" + cookie[1])

    def get_cookie_from_file(self):
        cookies = {}  # 初始化cookies字典变量
        if self.cookies_cache != None:
            name, value = self.cookies_cache.strip().split('=', 1)
            cookies[name] = value  # 为字典cookies添加内容
        return cookies
        # cookies = {}  # 初始化cookies字典变量
        # for line in self.cookies_set:
        #     name, value = line.strip().split('=', 1)
        #     cookies[name] = value  # 为字典cookies添加内容
        # if os.path.exists(self.cookies_file):
        #     with open('cookies.txt', 'r') as f:
        #         for line in f.readlines():
        #             name, value = line.strip().split('=', 1)
        #             cookies[name] = value  # 为字典cookies添加内容
        # else:
        #     print("cookies不存在")
        print("get_cookie_from_file cookies = ", cookies)
        return cookies

    def getContentLength(self, playload):
        return len(urlencode(playload))

    def record_request(self, url, header, data, cookie):
        with open("./res/request_record.txt", 'a') as f:
            f.write("*************************************************************\n")
            f.write(url + "\n")
            f.write(str(header) + "\n")
            f.write(str(data) + "\n")
            f.write(str(cookie) + "\n")

class WebDataProcessor:
    ocr = None
    def __init__(self):
        self.ocr = ddddocr.DdddOcr(old=True)

    def getAuthcode(self, filepath):
        image = 'aaaa'
        with open(filepath, 'rb') as f:
            image = f.read()
        return self.ocr.classification(image)

    def getEncodePwd(self, pwd, key):
        des_obj = des(key[0 : 8], ECB, key[0 : 8], pad=None, padmode=PAD_PKCS5)
        secret_bytes = des_obj.encrypt(pwd, padmode=PAD_PKCS5)
        return base64.encodebytes(secret_bytes).decode().rstrip('\n')

    def parseKeyFromHtml(self, html):
        soup = BeautifulSoup(html, 'lxml')
        page = soup.find(attrs={"name": "lt"})
        return page['value']

if __name__ == "__main__":
    wdp = WebDataProcessor()
    pwd_str = wdp.getEncodePwd("084413", "LT-14675424-OcZtHP6YysrSbsHWmTe7S0ISfRIs0o-https://csxrz.cqnu.edu.cn/cas")
    print(pwd_str)
    # net = NetRequest()
    # data = {
    #     'username': "2021210516081",
    #     'password': "jHdNZuczguU=",
    #     'authCode': "T41r",
    #     'It': "LT-14675424-OcZtHP6YysrSbsHWmTe7S0ISfRIs0o-https://csxrz.cqnu.edu.cn/cas",
    #     "execution" : "e1s1",
    #     "_eventId" : "submit",
    #     'isQrSubmit': 'false',
    #     'qrValue': '',
    #     'isMobileLogin': 'false'
    # }
    # print(net.getContentLength(data))
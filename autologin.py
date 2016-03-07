import os
import urllib
import urllib2
import xml.etree.ElementTree as ET
try:
    import json
except ImportError:
    import simplejson as json

class autoLogin:
    def init(self):
        None

    def requestLogin(self,host,referUrl,loginUrl,user,pwd):
        cookiejar=cookielib.CookieJar()
        urlopener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        urllib2.install_opener(urlopener)
        urlopener.addheaders.append(('Referer', referUrl))
        urlopener.addheaders.append(('Accept-Language', 'zh-CN'))
        urlopener.addheaders.append(('Host', host))
        urlopener.addheaders.append(('User-Agent', 'Mozilla/5.0 (compatible; MISE 9.0; Windows NT 6.1); Trident/5.0'))
        urlopener.addheaders.append(('Connection', 'Keep-Alive'))

    def readConfig(self):
        with open('config.json','r') as configFile:
             config = configFile.read()
             print config
             jsonConfig = json.loads(config)
        return jsonConfig

    def login(self):
        config = self.readConfig()
        print config
        loginConfig = config['login']
        url = loginConfig['url']
        user = loginConfig['user']
        pwd = loginConfig['pwd']
    
    def log(self):
        None

    def downloadFile(self):
        None

if __name__=='__main__':
    autoLogin = autoLogin()
    autoLogin.login()
              



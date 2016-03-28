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

    def requestLogin(self,option):
        cookiejar=cookielib.CookieJar()
        urlopener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        urllib2.install_opener(urlopener)
        urlopener.addheaders.append(('Referer', option.referUrl))
        urlopener.addheaders.append(('Accept-Language', 'zh-CN'))
        urlopener.addheaders.append(('Host', option.host))
        urlopener.addheaders.append(('User-Agent', 'Mozilla/5.0 (compatible; MISE 9.0; Windows NT 6.1); Trident/5.0'))
        urlopener.addheaders.append(('Connection', 'Keep-Alive'))
        #downloadVodeImage(imageUrl,urlopener)
        #vocde = readVCode()
        requestData = {}
        replyContent = urlopener.open(urllib2.Request(option.loginUrl, urllib.urlencode(requestData)))
        result = replyContent.read(50000)

        if result.find('login.jsp') != -1:
            None
        else:
            None


    def downloadVCodeImage(self, imageUrl):
        None
        # try:
        #     toSaveFile=open(r'code.jpg', 'w')
        #     toSaveFile.write(urlopener.open(urllib2.Request(imageUrl)).read()
        #     toSaveFile.close()
        #     return True
        # except:
        #     return False

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
        # url = loginConfig['url']
        # user = loginConfig['user']
        # pwd = loginConfig['pwd']
        # host = loginConfig['host']
        # referUrl = loginConfig['referUrl']
        self.requestLogin(loginConfig);

    def log(self):
        None

    def downloadFile(self):
        None

if __name__=='__main__':
    autoLogin = autoLogin()
    autoLogin.login()

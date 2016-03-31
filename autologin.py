import os
import urllib
import urllib2
import cookielib
try:
    from BeautifulSoup import BeautifulSoup as BS
except ImportError:
    from bs4 import BeautifulSoup as BS
try:
    import json
except ImportError:
    import simplejson as json

class autoLogin:
    def init(self):
        None

    def requestLogin(self):
        None

    def downloadFile(self, fileUrl, fileName, urlopener):
        result=False

        try:
            if fileUrl:
                outfile=open(fileName, 'w')
                outfile.write(urlopener.open(urllib2.Request(fileUrl)).read())
                outfile.close()
                result=True
            else:
                print 'ERROR: fileUrl is NULL!'
        except:
            result=False
        return result

    def doLogin(self,option):
        cookiejar=cookielib.CookieJar()
        urlopener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))

        urllib2.install_opener(urlopener)

        print "option", option['referUrl']

        urlopener.addheaders.append(('Referer', option['referUrl']))
        urlopener.addheaders.append(('Accept-Language', 'zh-CN'))
        urlopener.addheaders.append(('Host', option['host']))
        urlopener.addheaders.append(('User-Agent', 'Mozilla/5.0 (compatible; MISE 9.0; Windows NT 6.1); Trident/5.0'))
        urlopener.addheaders.append(('Connection', 'Keep-Alive'))

        #downloadVodeImage(imageUrl,urlopener)
        #vocde = readVCode()
        #requestData = {}

        replyContent = urlopener.open(urllib2.Request(option['indexUrl']))
        result = replyContent.read(50000)


        print 'result', result

        pageHtml = BS(result)
        usernameInputNode = pageHtml.body.find('input',attrs={'id':'login'})
        passInputNode = pageHtml.body.find('input',attrs={'type':'password'})
        vcodeNode = pageHtml.body.find('input',attrs={'id':'verifyCode'})

        print usernameInputNode.get('name')
        pname = passInputNode.get('name')
        print vcodeNode.get('name')


        #download vcode image
        self.downloadFile(option['vcodeUrl'], os.path.join(option['tempDir'], "vcode.png"), urlopener)
        #form the request data
        loginData={
                    'clientinfo':"",
                    'info':"",
                    'cmd':"already-registered",
                    'login':option['user']
                }
        loginData[pname] = option['pwd']
        loginData['verifyCode'] = raw_input('verify code')
        loginReply = urlopener.open(urllib2.Request(option['loginUrl'], urllib.urlencode(loginData)))
        loginResultHtml=loginReply.read(500000)

        print '---- loginResultHtml ---'
        print loginResultHtml

        # if result.find('login.jsp') != -1:
        #     None
        # else:
        #     None


    def readConfig(self):
        with open('config.json','r') as configFile:
             config = configFile.read()
             jsonConfig = json.loads(config)
        return jsonConfig

    def login(self):
        config = self.readConfig()

        loginConfig = config['login']
        print loginConfig
        # url = loginConfig['url']
        # user = loginConfig['user']
        # pwd = loginConfig['pwd']
        # host = loginConfig['host']
        # referUrl = loginConfig['referUrl']
        self.doLogin(loginConfig);

    def log(self):
        None

if __name__=='__main__':
    autoLogin = autoLogin()
    autoLogin.login()

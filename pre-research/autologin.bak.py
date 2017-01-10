#coding=utf8

import os
import urllib
import urllib2
import cookielib
import pytesseract
from PIL import Image

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

    def crackVCode(self, vcodeUrl, tempDir, fileName, urlopener):
        result=False

        try:
            if vcodeUrl:
                pngFileName = os.path.join(tempDir, fileName+'.png')
                outfile=open(pngFileName, 'w')
                outfile.write(urlopener.open(urllib2.Request(vcodeUrl)).read())
                outfile.close()

                png = Image.open(pngFileName)
                png.load()
                bg=Image.new("RGB", png.size, (255, 255, 255))
                bg.paste(png, mask=png.split()[3])

                jpgFileName = os.path.join(tempDir, fileName+'.jpg')
                bg.save(jpgFileName, 'JPEG', quality=80)
                image = Image.open(jpgFileName)
                result = pytesseract.image_to_string(image)
            else:
                print 'ERROR: fileUrl is NULL!'
        except Exception,e:
            print 'Exception', e
            result=None
        return result

    def doLogin(self,option):
        cookieFile = 'cookie'
        #cookiejar=cookielib.CookieJar()
        cookiejar = cookielib.MozillaCookieJar(cookieFile)
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

        #print usernameInputNode.get('name')
        pname = passInputNode.get('name')
        #print vcodeNode.get('name')


        #download vcode image and crack it
        tempDir = option['tempDir']
        vcode = self.crackVCode(option['vcodeUrl'], tempDir, "vcode", urlopener)

        #form the request data
        loginData={
                    'clientinfo':"",
                    'info':"",
                    'cmd':"already-registered",
                    'tabs1':"already-registered",
                    'login':option['user']
                }

        loginData[pname] = option['pwd']
        loginData['verifyCode'] = vcode.strip()

        print 'loginData'
        print loginData

        loginReply = urlopener.open(urllib2.Request(option['loginUrl'], urllib.urlencode(loginData)))
        loginResultHtml=loginReply.read(500000)

        resultPage = BS(loginResultHtml)
        vcodeNode = resultPage.body.find('input',attrs={'id':'verifyCode'})

        if vcodeNode == None:
            print 'Done'
            #print loginResultHtml
            cookiejar.save(ignore_discard=True, ignore_expires=True)
            sessionId = ''
            for cookie in cookiejar:
                if cookie.name == 'JSESSIONID':
                    sessionId = cookie.value
                print cookie.name, cookie.value, cookie.domain
            testData = """callCount=1
                            page=/html/nds/portal/ssv/index.jsp?ss=48
                            httpSessionId={0}
                            scriptSessionId=yfzhu441
                            c0-scriptName=Controller
                            c0-methodName=query
                            c0-id=0
                            c0-param0=string:%7B%22init_query%22%3A%20false%2C%20%22range%22%3A%2020%2C%20%22show_alert%22%3A%20true%2C%20%22start%22%3A%200%2C%20%22qlcid%22%3A%201047512%2C%20%22dir_perm%22%3A%201%2C%20%22fixedcolumns%22%3A%20%22%22%2C%20%22orders%22%3A%20%5B%7B%22d%22%3A%20%22%E6%8E%92%E5%90%8D%22%2C%20%22c%22%3A%20%22V_STORERETAILORDERDAY.ORDERNO%22%7D%5D%2C%20%22table%22%3A%20%22V_STORERETAILORDERDAY%22%2C%20%22callbackEvent%22%3A%20%22RefreshGrid%22%2C%20%22subtotal%22%3A%20true%2C%20%22param_str2%22%3A%20%22table%3D99922374%26tab_count%3D1%26return_type%3Dn%26accepter_id%3Dnull%26qlcid%3D1047512%26param_count%3D3%26resulthandler%3D%252Fhtml%252Fnds%252Fportal%252Ftable_list.jsp%26show_maintableid%3Dtrue%26V_STORERETAILORDERDAY.DATEDESC%3D20160424~20160501%26V_STORERETAILORDERDAY.DATEDESC_1%3D20160424%26V_STORERETAILORDERDAY.DATEDESC_2%3D20160501%26V_STORERETAILORDERDAY.C_STORE_ID%3D%26V_STORERETAILORDERDAY.C_STORE_ID%252Fsql%3D%26V_STORERETAILORDERDAY.C_STORE_ID%252Ffilter%3D%26V_STORERETAILORDERDAY.ORDERNO%3D%26show_all%3Dtrue%26queryindex_-1%3D-1%22%2C%20%22resulthandler%22%3A%20%22%2Fhtml%2Fnds%2Fportal%2Ftable_result.jsp%22%2C%20%22totalRowCount%22%3A%2024%7D
                            batchId=3""".format(sessionId)
            print 'testData', testData


            req = urllib2.Request("http://portal.grn.cn/servlets/dwr/call/plaincall/Controller.query.dwr", testData)
            req.add_header('Referer', 'http://portal.grn.cn/html/nds/portal/ssv/index.jsp?ss=48')
            req.add_header('Content-Type', 'text/plain')

            testReply = urlopener.open(req)
            testReplyHtml=testReply.read(500000)
            print '---- testReplyHtml ---'
            print testReplyHtml

            if result.find('login.jsp') != -1:
                None
            else:
                None
        else:
            print 'Login Failed'



        # testReply = urlopener.open(urllib2.Request("http://portal.grn.cn/html/nds/object/object.jsp?table=99922374&&fixedcolumns=&id=4918127", urllib.urlencode(loginData)))
        # testReplyHtml=testReply.read(500000)
        # print '---- testReplyHtml ---'
        # print testReplyHtml

        # if result.find('login.jsp') != -1:
        #     None
        # else:
        #     None

    def testCookieLogin(self):
        cookiejar = cookielib.MozillaCookieJar()
        cookiejar.load('cookie', ignore_discard=True, ignore_expires=True)
        urlopener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        urllib2.install_opener(urlopener)
        testReply = urlopener.open(urllib2.Request("http://portal.grn.cn/html/nds/object/object.jsp?table=99922374&&fixedcolumns=&id=4918127"))
        testReplyHtml=testReply.read(500000)
        print '---- testReplyHtml ---'
        print testReplyHtml

    def readConfig(self):
        with open('config.json','r') as configFile:
             config = configFile.read()
             jsonConfig = json.loads(config)
        return jsonConfig

    def login(self):
        config = self.readConfig()

        loginConfig = config['login']
        print loginConfig
        self.doLogin(loginConfig);
        #self.testCookieLogin()

    def log(self):
        None

if __name__=='__main__':
    autoLogin = autoLogin()
    autoLogin.login()

#coding=utf8

import requests
import os
import cookielib
import pytesseract
from PIL import Image
#from StringIO import StringIO

try:
    from BeautifulSoup import BeautifulSoup as BS
except ImportError:
    from bs4 import BeautifulSoup as BS
try:
    import json
except ImportError:
    import simplejson as json

class requestLogin:
    def init(self):
        None

    def crackVCode(self, vcodeUrl, tempDir, fileName, session):
        result=False

        try:
            if vcodeUrl:
                pngFileName = os.path.join(tempDir, fileName+'.png')
                outfile=open(pngFileName, 'w')
                resp = session.get(vcodeUrl)
                outfile.write(resp.content)
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
        cookiejar = cookielib.MozillaCookieJar(cookieFile)
        headers = {
            'Referer': option['referUrl'],
            'Accept-Language': 'zh-CN',
            'Host': option['host'],
            'User-Agent': 'Mozilla/5.0 (compatible; MISE 9.0; Windows NT 6.1); Trident/5.0',
            'Connection': 'Keep-Alive'
        }

        session = requests.Session()
        resp = session.get(option['indexUrl'], headers=headers, cookies=cookiejar)
        result = resp.text

        pageHtml = BS(result)
        usernameInputNode = pageHtml.body.find('input',attrs={'id':'login'})
        passInputNode = pageHtml.body.find('input',attrs={'type':'password'})
        vcodeNode = pageHtml.body.find('input',attrs={'id':'verifyCode'})

        pname = passInputNode.get('name')

        tempDir = option['tempDir']
        vcode = self.crackVCode(option['vcodeUrl'], tempDir, "vcode", session)

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

        resp = session.post(option['loginUrl'], data=loginData)
        result = resp.text

        # print 'login result'
        # print result

        cookies = session.cookies.get_dict()
        testData = "callCount=1" + "\npage=/html/nds/portal/ssv/index.jsp?ss=48" + "\nhttpSessionId={0}".format(cookies['JSESSIONID'])
        testData = testData  + "\nscriptSessionId=yfzhu441"
        testData = testData  + "\nc0-scriptName=Controller"
        testData = testData  + "\nc0-methodName=query"
        testData = testData  + "\nc0-id=0"
        testData = testData  + "\nc0-param0=string:%7B%22init_query%22%3A%20false%2C%20%22range%22%3A%2020%2C%20%22show_alert%22%3A%20true%2C%20%22start%22%3A%200%2C%20%22qlcid%22%3A%201047512%2C%20%22dir_perm%22%3A%201%2C%20%22fixedcolumns%22%3A%20%22%22%2C%20%22orders%22%3A%20%5B%7B%22d%22%3A%20%22%E6%8E%92%E5%90%8D%22%2C%20%22c%22%3A%20%22V_STORERETAILORDERDAY.ORDERNO%22%7D%5D%2C%20%22table%22%3A%20%22V_STORERETAILORDERDAY%22%2C%20%22callbackEvent%22%3A%20%22RefreshGrid%22%2C%20%22subtotal%22%3A%20true%2C%20%22param_str2%22%3A%20%22table%3D99922374%26tab_count%3D1%26return_type%3Dn%26accepter_id%3Dnull%26qlcid%3D1047512%26param_count%3D3%26resulthandler%3D%252Fhtml%252Fnds%252Fportal%252Ftable_list.jsp%26show_maintableid%3Dtrue%26V_STORERETAILORDERDAY.DATEDESC%3D20160424~20160501%26V_STORERETAILORDERDAY.DATEDESC_1%3D20160424%26V_STORERETAILORDERDAY.DATEDESC_2%3D20160501%26V_STORERETAILORDERDAY.C_STORE_ID%3D%26V_STORERETAILORDERDAY.C_STORE_ID%252Fsql%3D%26V_STORERETAILORDERDAY.C_STORE_ID%252Ffilter%3D%26V_STORERETAILORDERDAY.ORDERNO%3D%26show_all%3Dtrue%26queryindex_-1%3D-1%22%2C%20%22resulthandler%22%3A%20%22%2Fhtml%2Fnds%2Fportal%2Ftable_result.jsp%22%2C%20%22totalRowCount%22%3A%2024%7D"
        testData = testData  + "\nbatchId=3"

        # testData = """callCount=1\npage=/html/nds/portal/ssv/index.jsp?ss=48\nhttpSessionId={0}""".format(cookies['JSESSIONID'])
        print 'testData', testData

        resp = session.post("http://portal.grn.cn/servlets/dwr/call/plaincall/Controller.query.dwr", testData, headers={'content-type': 'text/plain'})

        print 'data result'
        print resp.text

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

if __name__=='__main__':
    requestLogin = requestLogin()
    requestLogin.login()

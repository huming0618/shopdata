#coding=utf8
import codecs
import requests
from urllib import quote,unquote
import os
import cookielib
import pytesseract
from PIL import Image
import json
import execjs
import datetime
import uuid
import psycopg2

from config import config as task_config
#from StringIO import StringIO

try:
    from BeautifulSoup import BeautifulSoup as BS
except ImportError:
    from bs4 import BeautifulSoup as BS

try:
    import json
except ImportError:
    import simplejson as json

pytesseract.pytesseract.tesseract_cmd = task_config['tesseractBin']
# def _remoteHandleCallback(para1, para2, jsonText):
#     return json.loads(jsonText)

def checkLoginResult(result):
    if u"欢迎" in result:
        return True
    else:
        return False

class WebAgent:
    records = []

    def init(self):
        None

    def crackVCode(self, vcodeUrl, tempDir, fileName, session):
        result=False

        try:
            if vcodeUrl:
                if not os.path.exists(tempDir):
                    os.makedirs(tempDir)

                pngFileName = os.path.join(tempDir, fileName+'.png')
                outfile=open(pngFileName, 'wb')
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
            import traceback
            traceback.print_exc()
            print 'Exception when crack the vcode', e
            result=None
        return result

    def run(self,option):
        from_date = option['from']
        to_date = option['to']
        date_period = from_date + "~" + to_date
        config = task_config['login']

        cookieFile = 'cookie'
        cookiejar = cookielib.MozillaCookieJar(cookieFile)
        headers = {
            'Referer': config['referUrl'],
            'Accept-Language': 'zh-CN',
            'Host': config['host'],
            'User-Agent': 'Mozilla/5.0 (compatible; MISE 9.0; Windows NT 6.1); Trident/5.0',
            'Connection': 'Keep-Alive'
        }

        session = requests.Session()
        resp = session.get(config['indexUrl'], headers=headers, cookies=cookiejar)
        result = resp.text

        pageHtml = BS(result, "lxml")
        usernameInputNode = pageHtml.body.find('input',attrs={'id':'login'})
        passInputNode = pageHtml.body.find('input',attrs={'type':'password'})
        vcodeNode = pageHtml.body.find('input',attrs={'id':'verifyCode'})

        pname = passInputNode.get('name')

        tempDir = config['tempDir']
        vcode = self.crackVCode(config['vcodeUrl'], tempDir, str(uuid.uuid4()), session)

        loginData={
                    'clientinfo':"",
                    'info':"",
                    'cmd':"already-registered",
                    'tabs1':"already-registered",
                    'login':config['user']
                }
        loginData[pname] = config['pwd']
        loginData['verifyCode'] = vcode.strip()

        # print 'loginData'
        # print loginData

        resp = session.post(config['loginUrl'], data=loginData)
        result = resp.text


        #print resp.text.encode('utf-8')
        with codecs.open("out.html", 'w', 'utf-8') as out:
            out.write(result)

        if checkLoginResult(result):
            print "OK.Logined"
        else:
            print "Login Failed"

if __name__ == "__main__":
    option = {'from': '2016-11-01', 'to': '2016-11-18'}
    # print option
    
    agent = WebAgent()
    agent.run(option)
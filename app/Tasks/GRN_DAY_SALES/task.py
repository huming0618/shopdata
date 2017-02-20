#coding=utf8

import requests
from urllib import quote,unquote
import os
import cookielib
import pytesseract
from PIL import Image
import json
import execjs
import argparse
import datetime
import uuid

#from StringIO import StringIO

try:
    from BeautifulSoup import BeautifulSoup as BS
except ImportError:
    from bs4 import BeautifulSoup as BS

try:
    import json
except ImportError:
    import simplejson as json

# def _remoteHandleCallback(para1, para2, jsonText):
#     return json.loads(jsonText)


class DaySaleTask:
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

    def run(self,option):
        from_date = option['from']
        to_date = option['to']
        date_period = from_date + "~" + to_date
        config = self.readConfig()['login']

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

        pageHtml = BS(result)
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

        # print 'login result'
        # print result


        testDataQueryParam = quote(json.dumps({
                            "init_query": "false",
                            "range": 1000000,
                            "show_alert": "true",
                            "start": 0,
                            "qlcid": 1047512,
                            "dir_perm": 1,
                            "fixedcolumns": "",
                            "orders": [{"d": "排名", "c": "V_STORERETAILORDERDAY.ORDERNO"}],
                            "table": "V_STORERETAILORDERDAY",
                            "callbackEvent": "RefreshGrid",
                            "subtotal": "true",
                            "param_str2": "table=99922374&tab_count=1&return_type=n&accepter_id=null&qlcid=1047512&param_count=3&resulthandler=%2Fhtml%2Fnds%2Fportal%2Ftable_list.jsp&show_maintableid=true&V_STORERETAILORDERDAY.DATEDESC=" + date_period + "&V_STORERETAILORDERDAY.DATEDESC_1=" + from_date + "&V_STORERETAILORDERDAY.DATEDESC_2=" + to_date + "&V_STORERETAILORDERDAY.C_STORE_ID=&V_STORERETAILORDERDAY.C_STORE_ID%2Fsql=&V_STORERETAILORDERDAY.C_STORE_ID%2Ffilter=&V_STORERETAILORDERDAY.ORDERNO=&show_all=true&queryindex_-1=-1",
                            "totalRowCount": 1
                        }));

        cookies = session.cookies.get_dict()
        testData = "callCount=1" + "\npage=/html/nds/portal/ssv/index.jsp?ss=48" + "\nhttpSessionId={0}".format(cookies['JSESSIONID'])
        testData = testData  + "\nscriptSessionId=yfzhu441"
        testData = testData  + "\nc0-scriptName=Controller"
        testData = testData  + "\nc0-methodName=query"
        testData = testData  + "\nc0-id=0"
        testData = testData + "\n" + "c0-param0=string:{0}".format(testDataQueryParam)
        #testData = testData  + "\nc0-param0=string:%7B%22init_query%22%3A%20false%2C%20%22range%22%3A%2020%2C%20%22show_alert%22%3A%20true%2C%20%22start%22%3A%200%2C%20%22qlcid%22%3A%201047512%2C%20%22dir_perm%22%3A%201%2C%20%22fixedcolumns%22%3A%20%22%22%2C%20%22orders%22%3A%20%5B%7B%22d%22%3A%20%22%E6%8E%92%E5%90%8D%22%2C%20%22c%22%3A%20%22V_STORERETAILORDERDAY.ORDERNO%22%7D%5D%2C%20%22table%22%3A%20%22V_STORERETAILORDERDAY%22%2C%20%22callbackEvent%22%3A%20%22RefreshGrid%22%2C%20%22subtotal%22%3A%20true%2C%20%22param_str2%22%3A%20%22table%3D99922374%26tab_count%3D1%26return_type%3Dn%26accepter_id%3Dnull%26qlcid%3D1047512%26param_count%3D3%26resulthandler%3D%252Fhtml%252Fnds%252Fportal%252Ftable_list.jsp%26show_maintableid%3Dtrue%26V_STORERETAILORDERDAY.DATEDESC%3D20160424~20160501%26V_STORERETAILORDERDAY.DATEDESC_1%3D20160424%26V_STORERETAILORDERDAY.DATEDESC_2%3D20160501%26V_STORERETAILORDERDAY.C_STORE_ID%3D%26V_STORERETAILORDERDAY.C_STORE_ID%252Fsql%3D%26V_STORERETAILORDERDAY.C_STORE_ID%252Ffilter%3D%26V_STORERETAILORDERDAY.ORDERNO%3D%26show_all%3Dtrue%26queryindex_-1%3D-1%22%2C%20%22resulthandler%22%3A%20%22%2Fhtml%2Fnds%2Fportal%2Ftable_result.jsp%22%2C%20%22totalRowCount%22%3A%2024%7D"
        testData = testData  + "\nbatchId=3"

        # testData = """callCount=1\npage=/html/nds/portal/ssv/index.jsp?ss=48\nhttpSessionId={0}""".format(cookies['JSESSIONID'])
        # print 'testData', testData

        resp = session.post("http://portal.grn.cn/servlets/dwr/call/plaincall/Controller.query.dwr", testData, headers={'content-type': 'text/plain'})

        # print 'data result'
        # print resp.text

        dwr_jsctx_source = None
        with open('jsctx.dwr.js') as js_file:
            dwr_jsctx = js_file.read() + resp.text


        ctx = execjs.compile(dwr_jsctx)

        result = ctx.call('getResult')
        error = ctx.call('getError')

        if error != None:
            # with open('test/test_resp_error.txt', 'w') as out:
            #     out.write(resp.text)
            print error
            raise Exception("Error - Failed to get the data: [Detail] %s " % error)
        else:
            with open('test_resp_%s-%s.txt' % (from_date, to_date), 'w') as out:
                out.write(resp.text)
            # print 'Result', result['data']
            # print type(result)
            sales_data = json.loads(json.dumps(result), encoding="utf-8")
            with open('test/test_resp.json', 'w') as out:
                out.write(json.dumps(sales_data))

            rows = sales_data['data']['rows']
            for row in rows:
                # print row
                # SAMPLE [19772456, 20161217, 3, u'\u62c9\u8428\u6797\u5ed3\u5317\u8def', 252660, 1, u'319.00', u'281.00', u'0.88', u'0.0000', u'0.0000', 1, u'281.00', u'1.00', None, None, u'2017/02/05 06:16:21', u'Y']
                order_id = row[0]
                order_date = row[1]
                order_rank = row[2]
                order_store = row[3]
                order_sumretailprice = row[6]
                order_sumsaleprice = row[7]
                order_avgdiscount = row[8]
                order_vipamt = row[9]
                order_vipradio = row[10]
                order_qty = row[11]
                order_avg_price = row[12]
                order_jst = row[13]
                order_updateon = row[16]
                order_status = row[17]

                # print order_store
                # print type(order_date)
            # print sales_data['data']['rows'][0][3]
            # print sales_data['data']['queryDesc']
            print "OK.DATA DOWNLOADED SUCCESSFULLY"

    def readConfig(self):
        with open('config.json','r') as configFile:
             config = configFile.read()
             jsonConfig = json.loads(config)
        return jsonConfig

def gevent_test():
    from gevent import monkey; monkey.patch_all()
    import gevent
    import time

    # def task1():
    #     task1 = DaySaleTask()
    #     task1.run({'from': "20161201", 'to': "20161218"})
    #
    # def task2():
    #     task1 = DaySaleTask()
    #     task1.run({'from': "20161101", 'to': "20161118"})
    #
    # def task3():
    #     task1 = DaySaleTask()
    #     task1.run({'from': "20160501", 'to': "20160518"})
    #
    # def task4():
    #     task1 = DaySaleTask()
    #     task1.run({'from': "20160701", 'to': "20160718"})


    def task1():
        task1 = DaySaleTask()
        task1.run({'from': "20160101", 'to': "20160301"})

    def task2():
        task1 = DaySaleTask()
        task1.run({'from': "20160302", 'to': "20160601"})

    def task3():
        task1 = DaySaleTask()
        task1.run({'from': "20160602", 'to': "20160901"})

    def task4():
        task1 = DaySaleTask()
        task1.run({'from': "20160902", 'to': "20170101"})

    start = time.time()
    tic = lambda: '%1.1f seconds ellapsed' % (time.time() - start)
    gevent.joinall([
        gevent.spawn(task1),
        gevent.spawn(task2),
        gevent.spawn(task3),
        gevent.spawn(task4)
    ])

    # task1()
    # task2()
    # task3()
    print tic()

def run_task(date_1, date_2):
    from gevent import monkey; monkey.patch_all()
    import gevent

    DIVIDER = 30

    from datetime import datetime
    from datetime import timedelta
    try:
        from_date = datetime.strptime(date_1, "%Y-%m-%d")
        to_date = datetime.strptime(date_2, "%Y-%m-%d")
    except ValueError as e:
        print "Invalid format of the date"

    if from_date > to_date:
        from_date,to_date = to_date,from_date

    days = (to_date - from_date).days

    start_date = from_date
    end_date = to_date

    points = range(0, days, DIVIDER)
    segments = []
    for x in points:
        print days, x
        end_date = start_date + timedelta(days=DIVIDER)
        if end_date > to_date:
            end_date = to_date
        segments.append((start_date, end_date))
        start_date = end_date + timedelta(days=1)

    def create_subtask(item):
        day1 = item[0].strftime("%Y%m%d")
        day2 = item[1].strftime("%Y%m%d")
        print day1, day2
        def run_subtask():
            task1 = DaySaleTask()
            task1.run({'from': day1, 'to': day2})
        return gevent.spawn(run_subtask)

    task_list = map(create_subtask, segments)
    gevent.joinall(task_list)
    # print segments


#python task.py --from 20161201 --to 20161218
if __name__=='__main__':

    # gevent_test()
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="start")
    parser.add_argument("--to", dest="end")
    arg = parser.parse_args()
    # print arg, type(arg)
    run_task(arg.start, arg.end)
    # option = {'from': arg.start, 'to': arg.end}
    # # print option
    #
    # task = DaySaleTask()
    # task.run(option)

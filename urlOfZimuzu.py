import requests
import re
import io
import webbrowser
import threading
from htmldom import htmldom

def myClick():
    headers={
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        #'Cookie':'',
        'Host': 'www.zimuzu.tv',
        #'Referer':'http://www.zimuzu.tv/user/login',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
        'X-Requested-With':'XMLHttpRequest'
    }
    index=s.get('http://www.zimuzu.tv/',verify=False,headers=headers)
    headers['Cookie']='srcurl=687474703a2f2f7777772e7a696d757a752e74762f;'+'yunsuo_session_verify='+requests.utils.dict_from_cookiejar(index.cookies)['yunsuo_session_verify']#此时已获取完整的header
    index=s.get('http://www.zimuzu.tv/?security_verify_data=313336362c373638'.strip(),headers=headers,verify=False)
    return headers

def trylogin(id,passwd):
    #登录
    postData = {
       'account':id,
       'password':passwd,
       'remember':'1',
       'url_back':'http://www.zimuzu.tv/user/user/index'
    }
    myurl = 'http://www.zimuzu.tv/User/Login/ajaxLogin'
    html = s.post(myurl,postData)#登录
    return html

#得到是否需要输入验证码，这次请求的相应有时会不同，有时需要验证有时不需要
def needIdenCode(id,passwd):
    html = trylogin(id,passwd)
    content = html.text
    #状态码为200，获取成功
    if html.status_code == 200:
        #print("获取请求成功")
        #\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801这六个字是请输入验证码的utf-8编码
        r = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801',re.S)
        result = re.search(r,content)
        #如果找到该字符，代表需要输入验证码
        if result:
            #print("此次安全验证异常，您需要输入验证码")
            return content
        #否则不需要
        else:
            #print("此次安全验证通过")
            return False

    else:
        pass
        #print("获取请求失败")

def getIdenCode(content):
    #得到验证码的图片
    r = re.compile('src="(.*?)')
    #匹配的结果
    matchResult = r.findall(content)
    print(matchResult)
    #已经匹配得到内容，并且验证码图片链接不为空
    if matchResult:
        return matchResult
    else:
        print("没有找到验证码内容")
        return False

def login(id,passwd):
    content = needIdenCode(id,passwd)
    if not content == False:
        #print("您需要手动输入验证码")
        matchResult = getIdenCode(content)
        if not matchResult == False:
            #print("验证码获取成功")
            #print("请在浏览器中输入您看到的验证码")
            webbrowser.open_new_tab(idenCode)
        else:
            pass
            #print("验证码获取失败，请重试")
    else:
        pass
        #print("不需要输入验证码")

def tostr(re,data):
    mylist = re.findall(data)
    mystr = ('').join(mylist)
    return mystr

def queryfornum(name):
    query = {
        'keyword':name,
        'search_type':''
    }
    half_url ='http://www.zimuzu.tv/search/index?'#url的不变部分
    html = s.post(half_url,query)
    data = html.text
    #print(data)
    r = re.compile(r'电视剧[^:]+')#正则表达式
    mystr = tostr(r,data)#提取了关键信息，但仍有无关信息
    r = re.compile(r'[0-9]')#再次处理的正则表达式
    num = tostr(r,mystr)#已获取关键信息
    #print(num)
    return num



def queryforhtml(num):
    half_url = 'http://www.zimuzu.tv/resource/list/'
    url = half_url + num#完整的查询url
    html = s.get(url)
    html.encoding = 'utf8'
    data = html.text
    return data

def myquery(name,lastvalue,seasonvalue):
    num = queryfornum(name)
    data = queryforhtml(num)
    #print(len(data))

    dom = htmldom.HtmlDom()
    lastvaluestr ="li[format="+lastvalue+"]"
    seasonvaluestr="li[season="+seasonvalue+"]"
    dom = dom.createDom(data)
    p = dom.find(lastvaluestr).filter(seasonvaluestr)
    parseddata = p.html()
    #print(parseddata)
    return parseddata

def writefile(filename,downloadurl):
    f = open(filename,"w")
    #print(filename)
    for d in downloadurl:
        f.write(d+'\n')
    f.close()


def saveurl1(data,path):
    r1=re.compile('(?<=a\shref\=")ed2k[^"]+')
    downloadurl=r1.findall(data)
    #print(downloadurl)
    filename = path+"电驴下载链接.txt"
    writefile(filename,downloadurl)

def saveurl2(data,path):
    r2=re.compile('(?<=a\shref\=")magnet[^"]+')
    downloadurl=r2.findall(data)
    #print(downloadurl)
    filename = path+"百度云下载链接.txt"
    writefile(filename,downloadurl)

def saveurl3(data,path):
    r3=re.compile('''(?<=xmhref\=")ed2k[^"]+''')
    downloadurl=r3.findall(data)
    #print(downloadurl)
    filename = path+"小米路由链接.txt"
    writefile(filename,downloadurl)

def saveurl4(data,path):
    r4=re.compile('''(?<=thunderhref\=")[^"]+''')
    downloadurl=r4.findall(data)
    #print(downloadurl)
    filename = path+"迅雷链接.txt"
    writefile(filename,downloadurl)

def saveurl5(data,path):
    r5=re.compile('''<a\shref\=".*?"\stype="ctdisk''')
    r9=re.compile('(?<=a\shref\=")[^"]+')
    r6=re.compile('''(?<=a\stype\="ctdisk"\shref\=")[^"]+''')
    down=tostr(r5,data)
    downloadurl1=r9.findall(down)
    downloadurl2=r6.findall(data)
    downloadurl=downloadurl1+downloadurl2
    #print(downloadurl)
    filename = path+"城通链接.txt"
    writefile(filename,downloadurl)

def saveurl6(data,path):
    r7=re.compile('''<a\shref\=".*?"\stype="disk''')
    r10=re.compile('(?<=a\shref\=")[^"]+')
    r8=re.compile('''(?<=a\stype\="disk"\shref\=")[^"]+''')
    down=tostr(r7,data)
    downloadurl3=r10.findall(down)
    downloadurl4=r8.findall(data)
    downloadurl=downloadurl3+downloadurl4
    #print(downloadurl)
    filename = path+"网盘链接.txt"
    writefile(filename,downloadurl)


def mkdir(path):
    import os
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        #print(path+' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        #print(path+' 目录已存在')
        return False


s=requests.session()
headers = myClick()
id = ''
passwd= ''
name = '权力的游戏'
lastvalue = "HDTV"
seasonvalue = "6"
login(id,passwd)
data=myquery(name,lastvalue,seasonvalue)
#print(data)
mkpath="g:\\"+name+"第"+seasonvalue+"季"+"\\"
# 调用函数
mkdir(mkpath)
threads = []
t1 = threading.Thread(target=saveurl1(data,mkpath))
t2 = threading.Thread(target=saveurl2(data,mkpath))
t3 = threading.Thread(target=saveurl3(data,mkpath))
t4 = threading.Thread(target=saveurl4(data,mkpath))
t5 = threading.Thread(target=saveurl5(data,mkpath))
t6 = threading.Thread(target=saveurl6(data,mkpath))
threads.append(t1)
threads.append(t2)
threads.append(t3)
threads.append(t4)
threads.append(t5)
threads.append(t6)
for t in threads:
    t.start()

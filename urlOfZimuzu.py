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
    headers['Cookie']='srcurl=687474703a2f2f7777772e7a696d757a752e74762f;'+'yunsuo_session_verify='+requests.utils.dict_from_cookiejar(index.cookies)['yunsuo_session_verify']#��ʱ�ѻ�ȡ������header
    index=s.get('http://www.zimuzu.tv/?security_verify_data=313336362c373638'.strip(),headers=headers,verify=False)
    return headers

def trylogin(id,passwd):
    #��¼
    postData = {
       'account':id,
       'password':passwd,
       'remember':'1',
       'url_back':'http://www.zimuzu.tv/user/user/index'
    }
    myurl = 'http://www.zimuzu.tv/User/Login/ajaxLogin'
    html = s.post(myurl,postData)#��¼
    return html

#�õ��Ƿ���Ҫ������֤�룬����������Ӧ��ʱ�᲻ͬ����ʱ��Ҫ��֤��ʱ����Ҫ
def needIdenCode(id,passwd):
    html = trylogin(id,passwd)
    content = html.text
    #״̬��Ϊ200����ȡ�ɹ�
    if html.status_code == 200:
        #print("��ȡ����ɹ�")
        #\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801������������������֤���utf-8����
        r = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801',re.S)
        result = re.search(r,content)
        #����ҵ����ַ���������Ҫ������֤��
        if result:
            #print("�˴ΰ�ȫ��֤�쳣������Ҫ������֤��")
            return content
        #������Ҫ
        else:
            #print("�˴ΰ�ȫ��֤ͨ��")
            return False

    else:
        pass
        #print("��ȡ����ʧ��")

def getIdenCode(content):
    #�õ���֤���ͼƬ
    r = re.compile('src="(.*?)')
    #ƥ��Ľ��
    matchResult = r.findall(content)
    print(matchResult)
    #�Ѿ�ƥ��õ����ݣ�������֤��ͼƬ���Ӳ�Ϊ��
    if matchResult:
        return matchResult
    else:
        print("û���ҵ���֤������")
        return False

def login(id,passwd):
    content = needIdenCode(id,passwd)
    if not content == False:
        #print("����Ҫ�ֶ�������֤��")
        matchResult = getIdenCode(content)
        if not matchResult == False:
            #print("��֤���ȡ�ɹ�")
            #print("�������������������������֤��")
            webbrowser.open_new_tab(idenCode)
        else:
            pass
            #print("��֤���ȡʧ�ܣ�������")
    else:
        pass
        #print("����Ҫ������֤��")

def tostr(re,data):
    mylist = re.findall(data)
    mystr = ('').join(mylist)
    return mystr

def queryfornum(name):
    query = {
        'keyword':name,
        'search_type':''
    }
    half_url ='http://www.zimuzu.tv/search/index?'#url�Ĳ��䲿��
    html = s.post(half_url,query)
    data = html.text
    #print(data)
    r = re.compile(r'���Ӿ�[^:]+')#������ʽ
    mystr = tostr(r,data)#��ȡ�˹ؼ���Ϣ���������޹���Ϣ
    r = re.compile(r'[0-9]')#�ٴδ����������ʽ
    num = tostr(r,mystr)#�ѻ�ȡ�ؼ���Ϣ
    #print(num)
    return num



def queryforhtml(num):
    half_url = 'http://www.zimuzu.tv/resource/list/'
    url = half_url + num#�����Ĳ�ѯurl
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
    filename = path+"��¿��������.txt"
    writefile(filename,downloadurl)

def saveurl2(data,path):
    r2=re.compile('(?<=a\shref\=")magnet[^"]+')
    downloadurl=r2.findall(data)
    #print(downloadurl)
    filename = path+"�ٶ�����������.txt"
    writefile(filename,downloadurl)

def saveurl3(data,path):
    r3=re.compile('''(?<=xmhref\=")ed2k[^"]+''')
    downloadurl=r3.findall(data)
    #print(downloadurl)
    filename = path+"С��·������.txt"
    writefile(filename,downloadurl)

def saveurl4(data,path):
    r4=re.compile('''(?<=thunderhref\=")[^"]+''')
    downloadurl=r4.findall(data)
    #print(downloadurl)
    filename = path+"Ѹ������.txt"
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
    filename = path+"��ͨ����.txt"
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
    filename = path+"��������.txt"
    writefile(filename,downloadurl)


def mkdir(path):
    import os
    # ȥ����λ�ո�
    path=path.strip()
    # ȥ��β�� \ ����
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        # ����������򴴽�Ŀ¼
        #print(path+' �����ɹ�')
        # ����Ŀ¼��������
        os.makedirs(path)
        return True
    else:
        # ���Ŀ¼�����򲻴���������ʾĿ¼�Ѵ���
        #print(path+' Ŀ¼�Ѵ���')
        return False


s=requests.session()
headers = myClick()
id = ''
passwd= ''
name = 'Ȩ������Ϸ'
lastvalue = "HDTV"
seasonvalue = "6"
login(id,passwd)
data=myquery(name,lastvalue,seasonvalue)
#print(data)
mkpath="g:\\"+name+"��"+seasonvalue+"��"+"\\"
# ���ú���
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

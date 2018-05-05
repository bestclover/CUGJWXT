import re
import execjs
import requests

def login(username,passwd):
    url1 = 'http://sfrz.cug.edu.cn/tpass/login?service=http%3A%2F%2Fxyfw.cug.edu.cn%2Ftp_up%2Fview%3Fm%3Dup#act=portal/viewhome'
    url2 = 'http://sfrz.cug.edu.cn/tpass/login?service=http%3A%2F%2Fxyfw.cug.edu.cn%2Ftp_up%2F'
    header2 = {
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Referer':'http://sfrz.cug.edu.cn/tpass/login?service=http%3A%2F%2Fxyfw.cug.edu.cn%2Ftp_up%2Fview%3Fm%3Dup',
        'Origin':'http://sfrz.cug.edu.cn',
        'Host':'sfrz.cug.edu.cn',
    }
    header1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    }
    ses = requests.session()
    res = ses.get(url=url1,headers=header1)
    res.encoding = 'utf-8'
    text = res.text
    parrtern1 = re.compile(r'<input type="hidden" id="lt" name="lt" value="(.*?)" />')
    parrtern2 = re.compile(r'<input type="hidden" name="execution" value="(.*?)" />')

    lt = re.search(parrtern1,text).group(1)
    execution = re.search(parrtern2,text).group(1)
    with open('des.js','r') as f:
        keys = execjs.compile(f.read()).call('strEnc', username+passwd+lt, '1', '2', '3')
    data = {
        'rsa': keys,
        'ul': str(len(username)),
        'pl': str(len(passwd)),
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit',
    }

    r = ses.post(url2,headers=header2,data=data)
    return ses



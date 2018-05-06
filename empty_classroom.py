import re
import time
from login import login

def getEmptyClassroom(num,username,passwd):
    '''
    zcd：周数代表数。256为当前周，此后周数代表数为256*n（如下一周为256*2，下两周为256*3）
    xqj: 星期代表数。2表示星期二
    jcd： 时间代表数之和。第一节为1，第二节为2，第三节为4，第四节为8，第五节为16，以此类推。如3则代表1+2,即第一节与第二节
    :param num: 如112会返回星期一第1、2节空闲教室。如果当前为周末，则返回下一星期的结果
    :return:
    '''
    if time.strftime('%w',time.localtime(time.time())) == '6' or time.strftime('%w',time.localtime(time.time())) == '5':
        week = 512
    else:
        week = 256
    day = int(num[0])
    first = int(num[1])-1
    second = int(num[2])-1
    Time = [
        1, 2, 4, 8, 16, 32, 64,
        128, 256, 512, 1024, 2048,
    ]
    url1 = 'http://202.114.207.137:80/ssoserver/login?ywxt=jw'
    url2 = 'http://jwgl.cug.edu.cn/jwglxt/cdjy/cdjy_cxKxcdlb.html?gnmkdm=N2155&layout=default&su=20171000737'
    url3 = 'http://jwgl.cug.edu.cn/jwglxt/cdjy/cdjy_cxKxcdlb.html?doType=query&gnmkdm=N2155'
    data = {
        'fwzt': 'cx',
        'xqh_id': 1,
        'xnm': 2017,
        'xqm': 12,
        'zcd': week,
        'xqj': day,
        'jcd': Time[first] + Time[second],
        'jyfs': 0,
        '_search':'false',
        'nd':int(time.time()*1000),
        'queryModel.showCount': 100,
        'queryModel.currentPage': 1,
        'queryModel.sortName': 'cdbh',
        'queryModel.sortOrder': 'asc',
        'time': 1,
    }
    ses = login(username, passwd)
    res = ses.get(url1)
    res = ses.get(url2)
    res = ses.post(url3,data=data)
    pattern = re.compile(r'"cdmc":"([^艺媒楼\d{3,5}].*?)"')
    classRoom = re.findall(pattern, res.text)
    return classRoom

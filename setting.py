# -*- coding: utf-8 -*-
# 程序设置

import requests
import logging
import sys
import logging
import yaml
import time
import execjs
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from io import BytesIO

# 从 YAML 文件读取配置
with open("setting.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

'''
需要配置的属性有:
1. user_id: 学号
2. cookie,token这两个字段需要在浏览器登录后，打开开发者工具，选择在network选项卡中选择recommendedCourse.do
   然后再找出相应字段
3. 你要选择的课程，类比相关格式，填写courses
4. 然后设置抢课延迟和选课提交次数
'''

'''
【个人附加批注】
流程：1.运行download_data.py拉取最新课程信息。2.查看信息按照格式填写setting.py。3.运行main.py进行抢课。
ps.第一步可以不用，改为F12直接查看id。
'''
# 日志文件级别
# logging_level = logging.INFO

#学号
user_id:str = str(config['user']['id'])

#每次重新登录后会改变
# cookie = '''

# '''

# 此字段自动获取，无需填写
# electiveBatchCode = "04a79c9569de4ac09f6826f6324a644a"

#每次重新登录后会改变
# token = '''

# '''

# 你要抢的课程，按照如下格式提前先填写好   !!!!!其实不更新课程列表也可以.....F12看id就好......
# courses =[
#     #id的意思是2023-2024学期+课程编号+课序号，  备注【选填】
#     {'id':'202320242150294000101','name':"信息检索(潘微科)"},
#     # {'id':'xxxxxxxxxxxxxxxxxxxxx','name':"高等数学(某某某)"},
#     # {'id':'xxxxxxxxxxxxxxxxxxxxx','name':"某课程(某某某)"},
# ]
# 抢课的顺序是从上到下，若上面的课程没抢到就不会往下抢，想改成循环的话可以重构一下main.py（更新：已重构完成  归忆）

courses = [str(i) for i in config['courses']]

# 间隔时间，单位是ms（最好不要低于400ms，不然可能会导致系统异常）
delay:int = int(config['network']['delay'])
# 抢课的次数
count:int = int(config['network']['count'])


########## 以上需要用户自行配置 ############
########## 以上需要用户自行配置 ############
########## 以上需要用户自行配置 ############


########## 不要修改下面的配置！！！！！！  ############
########## 不要修改下面的配置！！！！！！  ############
########## 不要修改下面的配置！！！！！！  ############

url:str = "http://bkxk.szu.edu.cn/"

logger = logging.getLogger("logger")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger.setLevel(config['logging']['level'].upper())
file_handler = logging.FileHandler(config['logging']['file'], encoding='utf-8')
file_handler.setFormatter(formatter)
file_handler.encoding = 'utf-8'
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(config['logging']['level'].upper())
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
headers:dict =  {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "bkxk.szu.edu.cn",
    "Pragma": "no-cache"
}

def get_encrypted_password(password):
    with open('des.min.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    encrypted_pwd = ctx.call("getPassword", password)
    return encrypted_pwd

session = requests.session()
session.headers.update(headers)

ts = int(time.time() * 1000)
vcode = session.post(
    url=f'{url}/xsxkapp/sys/xsxkapp/student/4/vcode.do?timestamp={ts}',
    data={'timestamp': str(ts)},
    headers=headers
)
image = session.get(f'{url}/xsxkapp/sys/xsxkapp/student/vcode/image.do?vtoken={vcode.json().get("data").get("token")}', headers=headers)
mpl.rcParams['toolbar'] = 'None'
img = mpimg.imread(BytesIO(image.content), format='jpg')
fig, ax = plt.subplots()
ax.imshow(img, )
ax.axis('off')
coords = []
def onclick(event):
    if event.xdata is None or event.ydata is None:
        return
    coords.append((f'{int(event.xdata)}-{int(event.ydata)}'))
    global verifyCode
    verifyCode = ','.join(coords)
    ax.plot(event.xdata, event.ydata, 'ro', markersize=8)
    fig.canvas.draw()
    if len(coords) == 4:
        fig.canvas.mpl_disconnect(cid)
        plt.close(fig)
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
login_data = {
    'loginName': config['user']['id'],
    'loginPwd': get_encrypted_password(config['user']['password']),
    'verifyCode': verifyCode,
    'vtoken': vcode.json().get("data").get("token")
}
response = session.post(f'{url}/xsxkapp/sys/xsxkapp/student/check/login.do', data=login_data, headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'DNT': '1',
    'Origin': 'http://bkxk.szu.edu.cn',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://bkxk.szu.edu.cn/xsxkapp/sys/xsxkapp/*default/index.do',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-gpc': '1',
})
logger.info(response.json().get('msg'))
headers['Cookie'] = '; '.join([f"{key}={value}" for key, value in session.cookies.get_dict().items()])
headers['Token'] = response.json().get('data').get('token')
try:
    myInfo = session.post(f'{url}xsxkapp/sys/xsxkapp/student/{config["user"]["id"]}.do',headers=headers).json()
    logger.debug(myInfo)
    electiveBatchCode = myInfo.get("data").get("electiveBatch").get("code")
    logger.info(f'{myInfo.get("data").get("name")}登录校验成功')
except:
    logger.error('校验失败，请检查学号，token，cookie是否填写正确')
    sys.exit(1)

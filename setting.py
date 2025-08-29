# -*- coding: utf-8 -*-
# 程序设置

'''
需要配置的属性有:
1. user_id: 学号
2. cookie,electiveBatchCode,token这三个字段需要在浏览器登录后，打开开发者工具，选择在network选项卡中选择recommendedCourse.do
   然后再找出相应字段
3. 你要选择的课程，类比相关格式，填写courses
4. 然后设置抢课延迟和选课提交次数
'''

'''
【个人附加批注】
流程：1.运行download_data.py拉取最新课程信息。2.查看信息按照格式填写setting.py。3.运行main.py进行抢课。
ps.第一步可以不用，改为F12直接查看id。
'''

#学号
user_id:str = "2021150047"

#每次重新登录后会改变
cookie = ("_WEU=rfhjF4PaYINuCCd_kqfaHvohaBAqdm4TgJ6RtIMKpLduDy1Ef2pMdvxDBRgFba2r; JSESSIONID=2CD85D58A90AA87245C9051B1E7976B5; "
          "b-user-id=c571adeb-8c51-f97f-3375-58c09fcab4df; insert_cookie=33374701")

electiveBatchCode = "04a79c9569de4ac09f6826f6324a644a"

#每次重新登录后会改变
token = "6e912f8e-a3b4-4ef5-8a0b-ca8358420b1c"

# 你要抢的课程，按照如下格式提前先填写好   !!!!!其实不更新课程列表也可以.....F12看id就好......
courses =[
    #id的意思是2023-2024学期+课程编号+课序号，  备注【选填】
    {'id':'202320242150294000101','name':"信息检索(潘微科)"},
    # {'id':'xxxxxxxxxxxxxxxxxxxxx','name':"高等数学(某某某)"},
    # {'id':'xxxxxxxxxxxxxxxxxxxxx','name':"某课程(某某某)"},
]
# 抢课的顺序是从上到下，若上面的课程没抢到就不会往下抢，想改成循环的话可以重构一下main.py（更新：已重构完成  归忆）

# 间隔时间，单位是ms（最好不要低于400ms，不然可能会导致系统异常）
delay:int = 400
# 抢课的次数
count:int = 150000000


########## 以上需要用户自行配置 ############
########## 以上需要用户自行配置 ############
########## 以上需要用户自行配置 ############





########## 不要修改下面的配置！！！！！！  ############
########## 不要修改下面的配置！！！！！！  ############
########## 不要修改下面的配置！！！！！！  ############

url:str = "http://bkxk.szu.edu.cn/"

headers:dict =  {
    "Cookie": cookie.strip(),
    "token": token.strip(),
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "bkxk.szu.edu.cn",
    "Pragma": "no-cache"
}



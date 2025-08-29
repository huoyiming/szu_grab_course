# -*- coding: utf-8 -*-
# 程序工具

import time
import requests
import setting
import json

session = requests.session()
session.headers.update(setting.headers)
current_milli_time = lambda: int(round(time.time() * 1000))


# 返回当前时间戳
def get_timestamp():
    return str(current_milli_time())
    
# Python 的模块就是天然的单例模式，因为模块在第一次导入时，会生成 .pyc 文件，当第二次导入时，就会直接加载 .pyc 文件，而不会再次执行模块代码。
# 返回session
def get_session():
    return session

# 获取完整路径
def get_url(relavie_path):
    return "{}{}".format(setting.url,relavie_path)

class Course:
    def __init__(self, id:str):
        self.id = id
        info = json.loads(session.post(
            get_url('xsxkapp/sys/xsxkapp/util/canchoose.do'),
            data={
                'xh': setting.user_id,
                'jxbid': self.id,
                'timestamp': get_timestamp()
            }).text)
        self.campus = info.get('data').get('campus')
        self.type = info.get('data').get('teachingClassType')
        data = {
            "data": {
            "studentCode": setting.user_id,
            "campus": "02",
            "electiveBatchCode": setting.electiveBatchCode,
            "isMajor": "1",
            "teachingClassType": "QXKC",
            "isMajor": "1",
            "queryContent": f"YCJX:2,MOOC:2,{self.id[9:-2]}"
            },
            "pageSize": "50",
            "pageNumber": "0",
            "order": "",
            "orderBy": "courseNumber"
        }
        form_data = {'querySetting': json.dumps(data), 'electiveBatchCode': setting.electiveBatchCode}
        resp = json.loads(session.post(
            get_url('xsxkapp/sys/xsxkapp/elective/queryCourse.do'),
            data=form_data
        ).text)
        classList = [i for i in resp.get('dataList') if i.get('courseNumber') == self.id[9:-2]]
        self.name = classList[int(self.id[-2:])-1].get('courseName')
        self.teacher = classList[int(self.id[-2:])-1].get('teacherName') if classList[int(self.id[-2:])-1].get('teachingClassID') == self.id else '教师获取失败'
    def choose(self):
        data = {
                "data": {
                    "operationType": "1",
                    "studentCode": setting.user_id,
                    "electiveBatchCode": setting.electiveBatchCode,
                    "teachingClassId": self.id,
                    "isMajor": "1",
                    "campus": self.campus,
                    "teachingClassType": self.type,
                    "chooseVolunteer": "1"
                }
            }
        form_data = {
            'addParam': json.dumps(data)
        }
        response = session.post(
            url=get_url("xsxkapp/sys/xsxkapp/elective/volunteer.do"),
            data=form_data,
            )
        return response.text
# -*- coding: utf-8 -*-
# 程序工具

import time
import requests
import setting
import json
import logging

logger = logging.getLogger("logger")

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
        logger.debug(f'初始化课程{id}')
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
        if not classList:
            logger.debug(f'课程信息获取失败：{self.id}')
            raise Exception('课程信息获取失败')
        self.name = classList[int(self.id[-2:])-1].get('courseName')
        self.teacher = classList[int(self.id[-2:])-1].get('teacherName') if classList[int(self.id[-2:])-1].get('teachingClassID') == self.id else '教师获取失败'
        logger.debug(f'课程信息：{self.name}({self.teacher})  校区：{self.campus}  类型：{self.type}')
    def choose(self):
        logger.debug(f'尝试选择课程 {self.name}({self.teacher})')
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
        logger.debug(f'选课请求返回：{response.text}')
        return response.json()
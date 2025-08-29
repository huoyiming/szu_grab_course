# -*- coding: utf-8 -*-
# 程序入口

# import downloads
import setting
import time
import sys
import choose_course
import util

if __name__ == "__main__":

    for i in range(setting.count):
        try:
            Courses = [util.Course(i['id']) for i in setting.courses]
            for course in Courses:
                response = course.choose()

                time.sleep(setting.delay/1000.0)
                
                if "该课程超过课容量" in response:
                    print(f"{course.name}({course.teacher}): 该课程超过课容量")
                    # break
                elif "添加选课志愿成功" in response:
                    print("抢课成功")
                    break
                else:
                    print(f"{course.name}({course.teacher}): "+response)

        except KeyboardInterrupt:
            print("通过键盘中断退出程序")
            sys.exit()
        except:
            print("出现错误，请检查设置setting.py部分是否填写正确")

    print("抢课结束")

    print("======================")
    print("您现在选课的结果如下")
    choose_course.query_result()

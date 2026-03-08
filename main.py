# -*- coding: utf-8 -*-
# 程序入口

# import downloads
import setting
import time
import sys
# import choose_course
import util
import traceback

logger = setting.logger
if __name__ == "__main__":
    Courses = []
    for i in range(setting.count):
        try:
            if not Courses:
                Courses = [util.Course(i) for i in setting.courses]
            for course in Courses:
                response = course.choose()

                time.sleep(setting.delay/1000.0)
                if "添加选课志愿成功" in response['msg']:
                    logger.warning(f"抢课成功: {course.name}({course.teacher})")
                    Courses.remove(course)
                    break
                elif response['msg'] == "该课程已经存在选课结果中":
                    logger.error(f"{course.name}({course.teacher}): {response['msg']}")
                else:
                    logger.info(f"{course.name}({course.teacher}): {response['msg']}")
            if not Courses:
                break

        except KeyboardInterrupt:
            logger.warning("通过键盘中断退出程序")
            sys.exit()
        except Exception as e:
            logger.error(f"出现错误: {e}，请检查设置setting.py部分是否填写正确")
            logger.debug(traceback.format_exc())
            time.sleep(setting.delay/1000.0)

    logger.info("抢课结束")

    # logger.info("======================")
    # logger.info("您现在选课的结果如下")
    # choose_course.query_result()

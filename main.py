# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    main
   Description :    主函数入口
   date        :    2021/5/11
-------------------------------------------------
"""
import random
import time
from libs.asyncSpider import Spider
from multiprocessing import Process
from utils.ffmpeg_converter import Converter


def m3u8_to_mp4():
    while 1:
        c = Converter()
        c.run()


def main():
    spider = Spider()
    if spider.ffmpeg.lower() == "true":
        # 启动ffmpeg转换
        p = Process(target=m3u8_to_mp4, )

        p.start()

    while 1:
        spider.run()
        time.sleep(random.randint(30, 1000))


if __name__ == '__main__':
    main()

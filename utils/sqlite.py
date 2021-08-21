# -*- coding: utf-8 -*-

import os
import configparser
from utils.logger import Logger
from peewee import *

log = Logger(filename="log/sqlite.log")
conf = configparser.ConfigParser()
cfg = "config.ini"
conf.read(cfg, encoding="utf-8")
dbPath = conf.get("sqlite", "path")
db = SqliteDatabase(dbPath)


class PornInfo(Model):
    video_id = IntegerField(unique=True, verbose_name="视频唯一编号")
    video_title = CharField(verbose_name="视频标题")
    video_site = CharField(max_length=1024, verbose_name="原始网址")
    video_thumb = CharField(max_length=1024, verbose_name="视频封面")
    video_m3u8 = CharField(max_length=1024, verbose_name="m3u8地址")
    video_Duration = CharField(verbose_name="视频时间")
    video_savepath = CharField(verbose_name="本地保存路径")
    crawl_status = BooleanField(default=False, verbose_name="ts爬取状态")
    ffmpeg_status = BooleanField(default=False, verbose_name="ffpemg mp4转换状态")

    class Meta:
        database = db


db.connect()
db.create_tables([PornInfo, ])

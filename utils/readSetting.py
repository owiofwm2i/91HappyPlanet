# -*- coding: utf-8 -*-

import configparser


class Config(object):

    def __init__(self):
        self.conf = configparser.ConfigParser()
        cfg = "config.ini"
        self.conf.read(cfg, encoding="utf-8")

        self.pornUrl = self.conf.get("91porn", "url")
        self.pornHost = self.conf.get("91porn", "host")

        self.dbPath = self.conf.get("sqlite", "path")
        self.savePath = self.conf.get("savepath", "save_path")
        self.ffmpeg=self.conf.get("ffmpeg","ffmpeg")

if __name__ == '__main__':
    a = Config()

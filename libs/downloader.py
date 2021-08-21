# -*- coding: utf-8 -*-

import base64
import os
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor, wait
from ipaddress import IPv4Address

import requests
from fake_useragent import UserAgent
from utils.logger import Logger
from utils.sqlite import PornInfo

ua = UserAgent()
log = Logger(filename="log/downloader.log")


class DownLoader(object):

    def __init__(self, save_path: None):
        self.save_path = save_path
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

    def m3u8s(self, url, **kwargs):
        """
        从m3u8文件中提取数据
        :param url:
        :return:
        """
        headers = {
            "User-Agent": ua.random,
            "Host": "91porn.com"
        }
        baseUrl = re.compile(r'(.*)/[0-9]+\.m3u8').search(url).group(1)
        fileName = re.compile(r'/([0-9]+)\.m3u8').search(url).group(1)
        if not os.path.exists("{}/{}".format(self.save_path, fileName)):
            os.mkdir("{}/{}".format(self.save_path, fileName))
            os.mkdir("{}/{}/m3u8".format(self.save_path, fileName))
            os.mkdir("{}/{}/ts".format(self.save_path, fileName))
        i = 0
        while i < 3:
            headers["X-Forwarded-For"] = str(IPv4Address(random.getrandbits(32)))
            r = requests.request("GET", url, headers=headers)
            if r.status_code != 400:
                with open("{}/{}/m3u8/{}.m3u8".format(self.save_path, fileName, fileName), "wb") as fp:
                    fp.write(r.content)

                with open("{}/{}/m3u8/{}.m3u8".format(self.save_path, fileName, fileName), "rb") as file:
                    urls = []
                    files = []
                    lines = file.readlines()
                    for line in lines:
                        if line.endswith(b".ts\n"):
                            urls.append(baseUrl + "/" + str(line.strip(b"\n")).replace("\'", "").replace("b", ""))
                            files.append(str(line.strip(b"\n")).replace("\'", "").replace("b", ""))

                # uploadUrl = github.uploadFile(fileName, "{}.m3u8".format(fileName), base64.b64encode(r.content))
                # if uploadUrl:
                #     log.logger.info("videoTitle:{}, videoDuration:{}, videoUrl:{}".format(kwargs.get("videoTitle"),
                #                                                                           kwargs.get("videoDuration"),
                #                                                                           uploadUrl))
                #     sql = '''INSERT INTO defaultVideo (videoId, videoTitle, videoUrl, videoDuration) VALUES ("%s", "%s", "%s", "%s")''' % (
                #     fileName, kwargs.get("videoTitle"), uploadUrl, kwargs.get("videoDuration"))
                #     log.logger.info("插入视频基本信息sql:{}".format(sql))
                #     db.insert(sql)
                return fileName, urls, files
            time.sleep(random.randint(2, 5))
            i += 1
            log.logger.warning("url:{}, 下载失败, 返回状态码结果:{}, 返回结果:{}, 重试次数:{}".format(url, r.status_code, r.text, i))

    def downVideo(self, tsFileName, tsUrl, file):
        """
        下载视频文件和缩略图
        :param tsFileName:
        :param tsUrl:
        :param file:
        :param thumbUrl:
        :return:
        """
        headers = {
            "User-Agent": ua.random,
            "Host": "91porn.com"
        }
        i = 0
        while i < 3:
            # 判断本地是否已经存在，存在的话跳过
            if os.path.exists("{}/{}/ts/{}".format(self.save_path, tsFileName, file)):
                log.logger.info("File:{}, 本地存在,跳过".format(file))

            headers["X-Forwarded-For"] = str(IPv4Address(random.getrandbits(32)))
            r = requests.request("GET", tsUrl, headers=headers)
            if r.status_code == 200:
                log.logger.info("下载ts文件:{}成功, 返回状态码:{}".format(file, r.status_code))

                # github.uploadFile(tsFileName, file, base64.b64encode(r.content))
                with open("{}/{}/ts/{}".format(self.save_path, tsFileName, file), "wb") as f:
                    f.write(r.content)
                break
            time.sleep(random.randint(2, 5))
            i += 1
            log.logger.warning("File:{}, 下载失败, 返回状态码结果:{}, 返回结果:{}, 重试次数:{}".format(file, r.status_code, r.text, i))

    def downThumb(self, tsFileName, thumbUrl, **kwargs):
        """
        下载封面
        :param tsFileName:
        :param thumbUrl:
        :param kwargs:
        :return:
        """
        headers = {
            "User-Agent": ua.random,
            "Host": "91porn.com"
        }
        thumbFileName = re.compile(r'/([0-9]+\.[a-z]+)').search(thumbUrl).group(1)

        i = 0
        while i < 3:
            # headers["X-Forwarded-For"] = str(IPv4Address(random.getrandbits(32)))
            # todo 下载这个封面还有问题
            r = requests.request("GET", thumbUrl, headers=headers)
            if r.status_code == 200:
                # uploadUrl = github.uploadFile(tsFileName, thumbFileName, base64.b64encode(r.content))
                # if uploadUrl:
                #     log.logger.info("videoTitle:{}, videoDuration:{}, videoThumbUrl:{}".format(kwargs.get("videoTitle"),
                #                                                                                kwargs.get(
                #                                                                                    "videoDuration"),
                #                                                                                uploadUrl))
                #     sql = '''update defaultVideo videoPic set value="%s" where videoId=%s''' % (uploadUrl, tsFileName)
                #     log.logger.info("插入图片封面链接sql:{}".format(sql))
                #     db.insert(sql)
                # todo 下载到本地
                pass
            time.sleep(random.randint(2, 5))
            i += 1
            log.logger.warning(
                "thumbUrl:{}, 下载失败, 返回状态码结果:{}, 返回结果:{}, 重试次数:{}".format(thumbUrl, r.status_code, r.text, i))

    def run(self, m3u8Url, thumbUrl, **kwargs):
        """
        下载器主函数
        :param m3u8Url:
        :param thumbUrl:
        :return:
        """
        pool = ThreadPoolExecutor(max_workers=20)
        futures = []
        # 去掉特殊字符的标题
        video_title = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "_",
                             kwargs.get("videoTitle"))
        tsFileName, tsUrls, tsFiles = self.m3u8s(m3u8Url, videoTitle=kwargs.get("videoTitle"),
                                                 videoDuration=kwargs.get("videoDuration"))
        if tsFileName:
            # self.downThumb(tsFileName, thumbUrl)
            for i in range(len(tsUrls)):
                tsUrl = tsUrls[i]
                tsFile = tsFiles[i]
                futures.append(pool.submit(self.downVideo, tsFileName, tsUrl, tsFile))
                time.sleep(random.random())
            wait(futures)

            # ts文件检查
            tsfile = "{}/{}/ts".format(self.save_path, tsFileName)
            tsm3u8 = "{}/{}/m3u8".format(self.save_path, tsFileName)
            file_folder = "{}/{}".format(self.save_path, tsFileName)
            wc_cmd = 'ls -l {} | grep "^-" | wc -l'.format(
                tsfile)
            result = os.popen(wc_cmd, 'r', 1)
            file_num = result.read().strip()
            crawl_status = False
            if int(file_num) == len(tsUrls):
                # todo 拼接，如果有FFmpeg可以重新写一个转换命令
                '''
                ffmpeg -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp,https" -i 507551.m38u -c copy out.mp4
                根据m38u文件来进行合并
                '''
                cat_cmd = "cp -r {}/*.ts {}/".format(tsfile, tsm3u8)
                os.system(cat_cmd)
                # 信息入库状态
                crawl_status = True
                # 删除零散的ts文件
                # rm_cmd = "rm -rf {}".format(tsfile)
                # os.system(rm_cmd)
                log.logger.warning("任务:{} 下载完成".format(m3u8Url))

            if PornInfo.select().where(PornInfo.video_id == tsFileName).count() == 0:
                # 没有数据，创建新库
                PornInfo.create(
                    video_id=tsFileName,
                    video_title=kwargs.get("videoTitle"),
                    video_site=kwargs.get("videoUrl"),
                    video_thumb=thumbUrl,
                    video_m3u8=m3u8Url,
                    video_Duration=kwargs.get("videoDuration"),
                    video_savepath=tsFileName,
                    crawl_status=crawl_status,
                )
            else:
                pron_info = PornInfo.select().where(PornInfo.video_id == tsFileName).get()
                pron_info.crawl_status = crawl_status
                pron_info.save()

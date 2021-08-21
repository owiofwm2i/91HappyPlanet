import random
import time

from utils.sqlite import PornInfo
import os
from utils.logger import Logger
import re

log = Logger(filename="log/converter.log")

import configparser

conf = configparser.ConfigParser()
cfg = "config.ini"
conf.read(cfg, encoding="utf-8")
save_path = conf.get("savepath", "save_path")


class Converter:

    def mission_get(self):
        try:
            mission = PornInfo.select().where(PornInfo.crawl_status == True and PornInfo.ffmpeg_status == False).get()
            return mission
        except Exception as e:
            log.logger.warning("暂时没有转换任务")
            return None

    def converter(self, input_path: str, output_path: str, new_filename: str,video_id:str) -> bool:
        # 如果是网络云盘还是有点读写问题，拷贝到本机，然后转换之后拷贝回去
        try:
            tmp_file_folder = "/tmp/{}".format(new_filename)
            if not os.path.exists(tmp_file_folder):
                os.mkdir(tmp_file_folder)
            mv_tmp_cmd = "cp {}/* {}".format(input_path, tmp_file_folder)
            os.system(mv_tmp_cmd)
            time.sleep(random.randint(1, 5))
            convert_cmd = "ffmpeg -y -i {}/{}.m3u8 -c copy  {}/{}.mp4".format(
                tmp_file_folder, video_id,tmp_file_folder, new_filename)
            result = os.popen(convert_cmd, 'r', 1)
            time.sleep(random.randint(10, 30))
            if "Error" in result.read().strip() or "Failed" in result.read().strip():
                return False
            else:
                # 移动到目标文件夹
                mv_cmd = "mv {}/{}.mp4 {}/{}.mp4".format(tmp_file_folder, new_filename, output_path, new_filename)
                os.system(mv_cmd)
                while 1:
                    if not os.path.exists("{}/{}.mp4".format(tmp_file_folder,new_filename)):
                        break
                    time.sleep(random.randint(1, 5))
                os.system("rm -r {}".format(tmp_file_folder))
                time.sleep(random.randint(1, 5))
                return True
        except Exception as e:
            log.logger.error("格式转换发生错误，原因:{}".format(e))
            return False

    def run(self):
        log.logger.info("ffmpeg convert process start...")
        while True:
            try:
                mission = self.mission_get()
                if mission == None:
                    time.sleep(random.randint(10, 60))
                    continue
                title = mission.video_title
                title = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "_",
                               title)
                m3u8_path = "{}/{}/m3u8".format(save_path, mission.video_savepath)
                output_path = "{}/{}".format(save_path, mission.video_savepath)
                convert_status = self.converter(m3u8_path, output_path, title, mission.video_id)
                if convert_status:
                    mission.ffmpeg_status = True
                    mission.save()
                    log.logger.info("{}转换为mp4成功,保存路径为{}/{}.mp4".format(title, output_path, title))
                else:
                    log.logger.error("{}转换为mp4失败,请检查ffmpeg是否在环境变量中")

                time.sleep(random.randint(0, 3))
            except Exception as e:
                time.sleep(random.randint(10, 60))
                continue

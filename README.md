# 91HappyPlanet
an unlimit 91pxxn crawler  ![visitors](https://visitor-badge.glitch.me/badge?page_id=91HappyPlanet)

## 运行环境
- 支持所有unix-like系统(也就是不支持windows)
- python3.5+ (becasue of async)

## 运行效果
- 91全站无限制爬虫
- 自动下载视频切片
- 自动转换为mp4(with ffmpeg support)


## 安装运行
### 配置config.ini文件
- 设置文件保存路径,比如 `/root/91` 最后不要带 **“/”** 符号 
- 如果机器安装好ffmpeg(如debian系可以为 `sudo apt install ffmpeg`, mac`brew insatll ffmpeg` etc)，可以设置相应选项为True，
### 安装以来库
- 安装依赖库`pip install -r requirements.txt`. 推荐使用虚拟环境
### 运行测试
- 简单运行 `python main.py`

## 错误解决

### fake_useragent.errors.FakeUserAgentError: Maximum amount of retries reached

下载 `https://fake-useragent.herokuapp.com/browsers/0.1.11` 并以后缀.json充命名
修改 `libs/downloader.py` 和 `libs/asyncSpider.py` 的
```python
a=UserAgent(path="刚才重命名的json路径")
```

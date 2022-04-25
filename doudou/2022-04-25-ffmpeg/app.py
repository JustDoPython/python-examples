# coding:utf-8

import ffmpeg

"""
path = 'main.mp4'
## 获取视频信息
probe = ffmpeg.probe(path)
video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
width = int(video_stream['width'])
height = int(video_stream['height'])
print(width, height)
print(video_stream)

## 视频镜像
ffmpeg.input(path).hflip().output('output.mp4').run()
ffmpeg.input(path).vflip().output('output.mp4').run()

## 添加底板
main = ffmpeg.input(path)
logo = ffmpeg.input('logo.png')
ffmpeg.filter([logo, main], 'overlay', 0, 500).output('out.mp4').run()

## 添加水印
main = ffmpeg.input(path)
logo = ffmpeg.input('logo.png')
ffmpeg.filter([main, logo], 'overlay', 0, 500).output('out.mp4').run()

## 视频截取
ffmpeg.input(path).trim(start_frame=10, end_frame=20).output('out3.mp4').run()

## 视频拼接
base = ffmpeg.input(path)
ffmpeg.concat(
    base.trim(start_frame=10, end_frame=20),
    base.trim(start_frame=30, end_frame=40),
    base.trim(start_frame=50, end_frame=60)
).output('out3.mp4').run()
"""
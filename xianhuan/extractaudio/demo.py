#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
#!/user/bin/env python
# coding=utf-8

from ffmpy import FFmpeg
import os
import uuid


def extract(video_path: str, tmp_dir: str, ext: str):
    file_name = '.'.join(os.path.basename(video_path).split('.')[0:-1])
    print('文件名:{}，提取音频'.format(file_name))
    return run_ffmpeg(video_path, os.path.join(tmp_dir, '{}.{}'.format(uuid.uuid4(), ext)), ext)

def run_ffmpeg(video_path: str, audio_path: str, format: str):
    ff = FFmpeg(inputs={video_path: None},
                outputs={audio_path: '-f {} -vn'.format(format)})
    ff.run()
    return audio_path

if __name__ == '__main__':
    print(extract('C:/个人/视频/aaa.mp4', 'C:/个人/视频', 'wav'))
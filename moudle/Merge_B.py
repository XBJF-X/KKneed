# coding=utf-8
import os
import subprocess

def merge():
    try:
        pid = os.getpid()
        with open(f"Log/{pid}/save_pathes.txt", "r",encoding="utf-8") as file:
            save_pathes = file.readlines()
            output_path = os.path.dirname(save_pathes[0])+"/"+"merged.mp4"
            video_clip = save_pathes[0].rstrip("\n")
            audio_clip = save_pathes[1].rstrip("\n")
            print(output_path)
            os.system(f'"C:/PythonProject/基于解析HTML文件下载合并流式传输视频（过滤广告）/bin/ffmpeg.exe" -i {video_clip} -i {audio_clip} -c:v copy -c:a copy -bsf:a aac_adtstoasc {output_path}')


    except FileNotFoundError as e:
        print(f"{e}")
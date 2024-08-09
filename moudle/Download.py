# coding=utf-8
import multiprocessing
import os
import sys
import time
from datetime import datetime

import requests
from tqdm import tqdm


def get_local_file_size(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size
    else:
        print("文件不存在或不是一个文件")


def get_file_size(url):
    response = requests.head(url)
    if response.status_code == 200:
        file_size = response.headers.get('Content-Length')
        if file_size:
            return int(file_size)
        else:
            print("无法获取文件大小")
    else:
        print(f"请求失败，状态码: {response.status_code}")


def download_file(url, dst_path, max_retries=30, delay=6):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True)
            with open(dst_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            break  # 下载成功，跳出循环
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                print(f"下载 {url} 超时3分种，已达到最大重试次数")
                print("继续下载会导致合成视频出现断节，请在网络良好时重新将HTML拖入窗口或重启脚本，本脚本支持续传")
                sys.exit()

def download():
    pid = os.getpid()

    try:
        with open(f"Log/{pid}/dst.txt", "r", errors='ignore', encoding="utf-8") as dst:
            dst1 = dst.read()
        def main():
            file_path = f'Log/{pid}/下载链接(filtered).txt'
            dst_dir = dst1  # 定义下载文件保存的目录
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            try:
                with open(file_path, 'r', ) as f:
                    urls = f.readlines()
            finally:
                # 确保文件被关闭
                pass  # 这里不需要做任何事情，因为 'with' 已经处理了关闭操作
            max_processes = 12
            pool = multiprocessing.Pool(processes=max_processes)
            count = 0
            count1 = 0
            count2 = 0
            in_progress = set()  # 用于跟踪正在执行的进程
            time1 = datetime.now()

            print("开始时间:", time1.strftime("%H:%M:%S"), end=" ")
            print(f"预计总下载任务数:{len(urls)}")
            print("下载位置:", dst_dir)

            # 创建进度条
            progress_bar = tqdm(total=len(urls),desc="下载进度",colour="CYAN", unit='个下载任务', unit_scale=True, ncols=100)


            for url in urls:
                url = url.strip()  # 去除每行的换行符
                file_name = os.path.basename(url).replace(".jpg", ".ts")

                dst_path = os.path.join(dst_dir, file_name)
                count = count + 1

                if os.path.exists(dst_path) == 0 or get_local_file_size(dst_path) <= 10240:
                    while len(in_progress) >= max_processes:
                        time.sleep(1)  # 等待进程完成
                        for proc in list(in_progress):
                            if proc.ready():
                                in_progress.remove(proc)
                    proc = pool.apply_async(download_file, args=(url, dst_path))
                    in_progress.add(proc)
                    count2 = count2 + 1
                else:
                    count1 = count1 + 1
                    print(f"第{count}项:{dst_path} 已存在，跳过下载。目前已跳过{count1}项下载")
                progress_bar.update(1)
            # 关闭进度条
            progress_bar.close()
            time2 = datetime.now()
            time3 = time2.strftime("%H:%M:%S")
            print(f"结束时间: {time3}", end=" ")
            print(f"实际总下载任务数:{count2}")
            timediff = time2 - time1
            total_seconds = timediff.total_seconds()
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)
            print(f"下载共耗时:{minutes}分{seconds}秒")
            pool.close()
            pool.join()



        main()
    except FileNotFoundError as e:
        print(f"{e}")

# coding=utf-8
import multiprocessing
import os
import re
import sys
import time
from datetime import datetime

import requests


def download_file(url, dst_path, max_retries=30, delay=6):
    headers = {
        "referer": "https://www.bilibili.com/",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
        "cookie": "buvid3=CE9632C5-615A-3ED7-F906-A6502B0CB04B28461infoc; b_nut=1702821628; _uuid=10CBC184E-449C-D8C4-6F14-4AD105D87F371028195infoc; buvid4=36200BDA-DEA8-2EB2-6AA8-3F4992EE066C29435-023121714-; enable_web_push=DISABLE; header_theme_version=CLOSE; CURRENT_FNVAL=4048; rpdid=|(u)YJm~l~m~0J'u~|JkR)~~~; buvid_fp_plain=undefined; FEED_LIVE_VERSION=V8; CURRENT_QUALITY=80; LIVE_BUVID=AUTO8317122246182757; PVID=1; SESSDATA=e002a3f3%2C1734068875%2C59b9f%2A62CjCDCTxs-u94Qodd7F5E2OEsNTD0GzYWh8h_Rb7qSKnEusNrhYVq548khvZ5HWHXWbESVmN6TGE0dDFVQkRNTFAySXY5TU9CaHhudldQamJIU1pOZmViQndMVmFzdU9YdTlYUWNJaGVKV2tRcng2WlNTdW41RGVwWFpzUVpPNExTalR6a2RYdzF3IIEC; bili_jct=3c02ead6019a85564bd61306f637835b; DedeUserID=398448576; DedeUserID__ckMd5=7adb385c03bcbf3b; is-2022-channel=1; fingerprint=de25f028dd8ebfe649ae25ba2bacd3b5; bp_t_offset_398448576=961786088316207104; home_feed_column=4; browser_resolution=1309-557; sid=842auvil; buvid_fp=bff5d92132552fb8895541092f5ba222; bsource=search_bing; b_lsid=7C10DC83D_1912B544978; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjMyNjg2NDYsImlhdCI6MTcyMzAwOTM4NiwicGx0IjotMX0.A42yGodZzrRXExTDnGzJksJ2XTYAL4msjY1_Y4doVkM; bili_ticket_expires=1723268586"
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True,headers=headers)
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
            dst_dir = dst1  # 定义下载文件保存的目录
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            try:
                with open(f'Log/{pid}/批量下载链接.txt', 'r', ) as f:
                    urls = f.readlines()
            finally:
                # 确保文件被关闭
                pass  # 这里不需要做任何事情，因为 'with' 已经处理了关闭操作
            max_processes = 1
            pool = multiprocessing.Pool(processes=max_processes)
            count = 0
            count1 = 0
            count2 = 0
            in_progress = set()  # 用于跟踪正在执行的进程
            time1 = datetime.now()
            print("开始时间:", time1.strftime("%H:%M:%S"), end=" ")
            print(f"预计总下载任务数:{len(urls)}")
            print("下载位置:", dst_dir)

            with open(f"Log/{pid}/save_pathes.txt","w",encoding="utf-8") as g:
                for url in urls:
                    url = url.strip("\n")  # 去除每行的换行符
                    url1 = os.path.basename(url)
                    pattern =".*?m4s"
                    file_name = re.findall(pattern, url1)
                    file_name1 = file_name[0]
                    save_path_1 = dst1 + file_name1
                    g.write(f"{save_path_1}\n")


                    count = count + 1

                    if os.path.exists(save_path_1) == 0 :
                        while len(in_progress) >= max_processes:
                            time.sleep(1)  # 等待进程完成
                            for proc in list(in_progress):
                                if proc.ready():
                                    in_progress.remove(proc)
                        proc = pool.apply_async(download_file, args=(url, save_path_1))
                        in_progress.add(proc)
                        count2 = count2 + 1
                    else:
                        count1 = count1 + 1
                        print(f"第{count}项:{save_path_1} 已存在，跳过下载。目前已跳过{count1}项下载")

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

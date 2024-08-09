# coding=utf-8
import os
import shutil
import sys
import time
from multiprocessing import Process, freeze_support

import moudle.Download_B
import moudle.FindDownloadAddress_B
import moudle.Merge_B
import moudle.RenameAndMove_B


def on_drop_full(Path):
    dir = os.path.dirname(Path)
    file_path = Path
    process1 = Process(target=on_drop_full_implement, args=(dir, file_path, downloadPath,))
    process1.start()
    #########注意！这段代码被注释掉就是多进程，不注释就是单进程！！！
    while process1.is_alive():
        time.sleep(1)

    print("继续监控监听文件夹下文件变化...")


def on_drop_full_implement(dir, file_path, downloadPath):
    pid = os.getpid()
    print(f"当前进程的PID为:{pid}")

    if not os.path.exists(f"Log/{pid}"):
        os.makedirs(f"Log/{pid}", exist_ok=True)
    else:
        shutil.rmtree(f"Log/{pid}")
        os.makedirs(f"Log/{pid}", exist_ok=True)

    with open("pid.txt", "w",encoding="utf-8") as pd:
        pd.write(str(pid))

    with open(f"Log/{pid}/src.txt", "w",encoding="utf-8") as src:
        src.write(file_path)
    with open(f"Log/{pid}/dst.txt", "w",encoding="utf-8") as dst:
        dst.write(dir + "/")
    if downloadPath != 0:
        with open(f"Log/{pid}/downloadPath.txt", "w",encoding="utf-8") as dp:
            dp.write(downloadPath + "/")

    moudle.FindDownloadAddress_B.get_download_address()
    moudle.Download_B.download()
    moudle.Merge_B.merge()
    moudle.RenameAndMove_B.rename_and_move()



def get_all_file_paths(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_paths=[]
    for root, dirs, files in os.walk(directory):  # 使用os.walk遍历目录及其子目录
        for file in files:  # 遍历当前目录下的所有文件
            if file.endswith(".html") :
                    file_paths.append(os.path.join(root, file).replace("\\", "/"))

    return file_paths

if __name__ == '__main__':
    freeze_support()
    pid=os.getpid()
    downloadPath = "G:/VIDEOS/B站"
    if not downloadPath :
        print("请填写Main.py中的下载目标目录（downloadPath）！！！")
        sys.exit()
    # 自己设定监听文件夹，反斜杠要换为正斜杠
    srcPath = "D:/桌面/爬取html"
    if not downloadPath :
        print("请填写Main.py中的监听目录（srcPath）！！！")
        sys.exit()
    file_paths = []  # 创建一个空列表用于存储文件路径
    processes_file_paths=[]
    print(f"当前进程PID为{pid}")
    print("请保证网络良好，超时3分钟将会中断下载任务，需要重新拖动HTML文件")
    print("开始监控监听文件夹下文件变化...")
    while True:
        try:
            file_paths=get_all_file_paths(srcPath)
            if len(file_paths) > 0:
                for path in file_paths.copy():
                    try:
                        if not path in processes_file_paths:
                            on_drop_full(path)
                            file_paths.remove(path)
                            processes_file_paths.append(path)
                    except Exception as e:
                        processes_file_paths.remove(path)
                        print("进程异常，已退出")
        except Exception as e:
            print("进程异常，已退出")
            sys.exit()
        time.sleep(3)

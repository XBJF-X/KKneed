import os
import shutil
import sys
import tkinter as tk
from multiprocessing import Process, freeze_support

from tkinterdnd2 import DND_FILES, TkinterDnD

import moudle.Download
import moudle.FilterAD
import moudle.FindDownloadAddress
import moudle.Merge
import moudle.RenameAndMove


def on_drop_full(event):

    dir = os.path.dirname(event.data.strip("{}"))
    file_path = event.data.strip("{}")


    # 如果没有正在运行的进程，则启动新的进程
    running_process = Process(target=on_drop_full_implement, args=(dir, file_path, downloadPath,))
    running_process.start()
    #########注意！这段代码被注释掉就是多进程，不注释就是单进程！！！
    # while running_process.is_alive():
    #     time.sleep(1)

    print("已处理完上一个HTML文件，继续等待拖放...")


def on_drop_full_implement(dir, file_path, downloadPath):
    pid = os.getpid()
    print(f"该进程的PID为:{pid}")


    if not os.path.exists(f"Log/{pid}"):
        os.makedirs(f"Log/{pid}", exist_ok=True)
    else:
        shutil.rmtree(f"Log/{pid}")
        os.makedirs(f"Log/{pid}", exist_ok=True)


    with open(f"Log/{pid}/src.txt", "w",encoding="utf-8") as src:
        src.write(file_path)
    with open(f"Log/{pid}/dst.txt", "w",encoding="utf-8") as dst:
        dst.write(dir + "/")
    if downloadPath != 0:
        with open(f"Log/{pid}/downloadPath.txt", "w",encoding="utf-8") as dp:
            dp.write(downloadPath + "/")

    moudle.FindDownloadAddress.find_download_address()
    moudle.FilterAD.filter_ad()
    moudle.Download.download()
    moudle.Merge.merge()
    moudle.RenameAndMove.rename_and_move()




def on_drop_only_RenameAndMove(event):
    dir = os.path.dirname(event.data.strip("{}"))
    file_path = event.data.strip("{}")



    running_process = Process(target=on_drop_only_RenameAndMove_implement, args=(dir, file_path, downloadPath,))
    running_process.start()
    #########注意！这段代码被注释掉就是多进程，不注释就是单进程！！！
    # while running_process.is_alive():
    #     time.sleep(1)

    print("已处理完上一个HTML文件，继续等待拖放...")



def on_drop_only_RenameAndMove_implement(dir, file_path, downloadPath):
    pid = os.getpid()
    print(f"该进程的PID为:{pid}")

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

    moudle.FindDownloadAddress.find_download_address()
    moudle.RenameAndMove.rename_and_move()

if __name__ == '__main__':
    freeze_support()
    downloadPath ="G:/VIDEOS/里番"
    if not downloadPath :
        print("请填写Main.py中的下载目标目录（downloadPath）！！！")
        sys.exit()
    print("请保证网络良好，超时3分钟将会中断下载任务，需要重新拖动HTML文件")
    print("等待HTML文件拖放...")

    # 创建根窗口，设置参数
    root = TkinterDnD.Tk()
    root.title("HTML处理窗口")
    root.geometry("250x100")

    # 创建两个Frame，用于划分窗口
    frame1 = tk.Frame(root, width=200, height=100, borderwidth=1, relief="solid")
    frame1.pack(side=tk.LEFT)

    frame2 = tk.Frame(root, width=200, height=100, borderwidth=1, relief="solid")
    frame2.pack(side=tk.RIGHT)

    # 为两个Frame添加标签
    label1 = tk.Label(frame1, text="完整的解析流程")
    label1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    label2 = tk.Label(frame2, text="仅重命名和移动")
    label2.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # 将拖放目标分别注册到两个Frame

    frame1.drop_target_register(DND_FILES)
    frame1.dnd_bind('<<Drop>>', on_drop_full)  # 绑定到左侧Frame
    frame2.drop_target_register(DND_FILES)
    frame2.dnd_bind('<<Drop>>', on_drop_only_RenameAndMove)  # 绑定到右侧Frame

    root.mainloop()



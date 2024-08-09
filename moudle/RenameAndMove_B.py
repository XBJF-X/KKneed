# coding=utf-8
import os
import shutil



def rename_and_move():
    pid = os.getpid()


    with open(f"Log/{pid}/downloadPath.txt", "r", encoding="utf-8") as f:
        download_path =f.read()
    with open(f"Log/{pid}/title.txt", "r", encoding="utf-8") as g:
        title = g.read()

    with open(f"Log/{pid}/save_pathes.txt", "r", encoding="utf-8") as file:

        save_pathes = file.readlines()
        output_path = os.path.dirname(save_pathes[0]) + "/" + "merged.mp4"
        download_path = download_path+title+".mp4"
        shutil.move(output_path, download_path)
        print(f"合并完成的视频已经移动到:{download_path}")
        for i in save_pathes:
            i=i.rstrip("\n")
            os.remove(i)
            print(f"{i}已删除")



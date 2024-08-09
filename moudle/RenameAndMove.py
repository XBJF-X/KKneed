# coding=utf-8
import os
import shutil




def find_element_position(lst, element):
    try:
        position = lst.index(element)
        return position
    except ValueError:
        return -1


def get_local_file_size(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size

def rename_and_move():
    pid = os.getpid()
    dst1 = ""
    try:
        with open(f"Log/{pid}/src.txt", "r", errors='ignore', encoding="utf-8") as src:
            src1 = src.read()
        with open(f"Log/{pid}/dst.txt", "r", errors='ignore', encoding="utf-8") as dst:
            dst1 = dst.read()
    except FileNotFoundError:
        pass

    list = dst1.replace("\\", "/").rstrip("/").split("/")
    index = find_element_position(list, "未完成")
    if index != -1:
        name_element = list[index + 1:]
        dst_element = list[:index] + list[index + 1:index + 2]

    try:
        new_name = " ".join(name_element)
        new_location = "/".join(dst_element)
    except NameError as e:
        print(f"{e}")

    # 把合并好的视频更名
    try:
        os.rename(f"{dst1}合成视频.mp4", f"{dst1}{new_name}.mp4")
    except FileNotFoundError:
        pass
    try:
        # 检验目标文件夹以及其下视频是否存在
        if not os.path.exists(f"{new_location}"):
            os.makedirs(f"{new_location}", exist_ok=True)
        if os.path.exists(f"{new_location}/{new_name}.mp4"):
            os.remove(f"{new_location}/{new_name}.mp4")

        os.rename(f"{dst1}{new_name}.mp4", f"{new_location}/{new_name}.mp4")

        if os.path.exists(f"{dst1}合成视频.mp4"):
            if get_local_file_size(f"{dst1}合成视频.mp4") <= 1024:
                os.remove(f"{dst1}合成视频.mp4")
        if os.path.exists(f"{dst1}{new_name}.mp4"):
            if get_local_file_size(f"{dst1}{new_name}.mp4") <= 1024:
                os.remove(f"{dst1}{new_name}.mp4")

        if os.path.exists(f"{new_location}/{new_name}.mp4"):
            if get_local_file_size(f"{new_location}/{new_name}.mp4") <= 1024:
                os.remove(f"{new_location}/{new_name}.mp4")
                print(f"文件 {new_location}/{new_name}.mp4 过小，已删除，稍后自动重新下载")
            else:
                print(f"合成视频已移动至 {new_location}/{new_name}.mp4")
                # 给解析过的网页更名并附上pid以便寻找
                new_src1 = os.path.dirname(src1)
                if len(os.path.basename(src1) + "-已解析" + str(pid) + new_name) >= 250:
                    new_suffix = os.path.basename(src1) + "-已解析" + str(pid)
                else:
                    new_suffix = os.path.basename(src1) + "-已解析" + str(pid) + new_name

                rename = "/".join([new_src1, new_suffix])
                if os.path.exists(rename):
                    os.remove(rename)
                    os.rename(src1, rename)
                else:
                    os.rename(src1, rename)

    except FileNotFoundError:
        print(f"移动至{new_location}失败")


    folder_path = src1.replace(".html", "_files")

    if os.path.exists(folder_path):# 确保文件夹存在
        # 递归删除文件夹及其内容
        shutil.rmtree(folder_path)
        print(f"文件夹 '{folder_path}' 及其内容已成功删除。\n进程已结束")
    else:
        print("进程已结束")

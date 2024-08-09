# coding=utf-8
import os

from moudle.Download import get_local_file_size


def merge():
    try:
        pid = os.getpid()

        # Open file

        with open(f"Log/{pid}/src.txt", "r",encoding="utf-8") as src:
            src1 = src.read()
        with open(f"Log/{pid}/dst.txt", "r", errors='ignore',encoding="utf-8") as dst:
            dst1 = dst.read()
        print("正在合并视频...\n当前操作的文件夹为:", dst1)
        with open(dst1 + "合成视频.mp4", "ab") as f:
            with open(f"Log/{pid}/下载链接(filtered).txt", "r") as filenames:

                while True:
                    line = filenames.readline()
                    filename = os.path.basename(line).replace(".jpg", ".ts")
                    dirname = os.path.dirname(line)

                    if not line:
                        break
                    else:
                        downLoadPath = os.path.join(dst1, filename).rstrip("\n")
                        if get_local_file_size(downLoadPath) <= 1024:
                            print(downLoadPath, "文件过小，可能是未下载完成的片段，请注意检查")
                        else:
                            try:
                                with open(downLoadPath, "rb") as g:
                                    f.write(g.read())
                            except FileNotFoundError:
                                new_filename = filename.rstrip("\n")
                                with open(f"Log/{pid}/log.txt", "a") as log:
                                    log.write(f"拼接视频时缺少{new_filename}\n")
                        try:
                            # 尝试删除文件
                            os.remove(downLoadPath)
                            with open(f"Log/{pid}/log.txt", "a") as log:
                                log.write(f"文件 {downLoadPath} 已成功删除。\n")
                        except FileNotFoundError:
                            # 如果文件不存在，忽略错误
                            with open(f"Log/{pid}/log.txt", "a") as log:
                                log.write(f"文件 {downLoadPath} 不存在，无需删除。\n")

                        except Exception as e:
                            # 捕获其他可能的异常
                            with open(f"Log/{pid}/log.txt", "a") as log:
                                log.write(f"删除文件时发生错误:{e}\n")
    except FileNotFoundError as e:
        print(f"{e}")
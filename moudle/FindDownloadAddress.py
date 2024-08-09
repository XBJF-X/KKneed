# coding=utf-8

import os

import requests
from bs4 import BeautifulSoup


def splicing(var1, var2):  # 把.ts文件的前半部分和后半部分去除重合部分之后拼接在一起
    # 以其中较短的字符串，从长到短依次循环匹配查找
    str1 = var1.rstrip("/")
    str1 = str1.replace("//", "/")
    str2 = var2.lstrip("/")
    f1 = ""
    for i in range(2, min(len(str1), len(str2))):
        if str1[-i:-1] + str1[-1] == str2[0:i]:
            f1 = str2[0:i]

    str3 = str1.replace(f1, "") + "/" + f1 + "/" + str2.replace(f1, "")
    str3 = str3.replace("//", "/")

    x = str3.find('/')
    # 在左边找到了反斜杠，则再加一个，保证以https://或者http://
    if x != -1:
        str3 = str3[:x] + "/" + str3[x:]
    return str3


def get_name_and_episode(content):
    with open(content, "r", errors='ignore', encoding="utf-8") as html:
        var = html.read().replace("\n", " ")
        # 匹配title标签
        start_index = var.find('<title>') + len("<title>")
        end_index = var.find('</title>')
        # 截取所需内容
        title = var[start_index:end_index].replace("\\", "")

        # 获取视频集数
        episode = []
        for i in range(0, len(title)):
            if title[i].isdigit():
                episode.append(title[i])
        if len(episode) > 0:
            episode_result = int("".join(episode))
        else:
            episode_result = "1"

        pre_suf_fix_lib = [("里番", "第"),("动漫电影","第"),("在线动漫","第"),("新旧番剧","第"),("","第")]
        start_index = 0
        end_index = -1

        for prefix, suffix in pre_suf_fix_lib:
            try:
                if prefix!="":
                    start_index = title.find(f'{prefix}') + len(f"{prefix}")
                    if start_index == -1:
                        start_index = 0
            except Exception as e:
                print(f"{e}")

            try:
                if suffix!="":
                    end_index = title.rfind(f'{suffix}')
            except Exception as e:
                print(f"{e}")
            if start_index != 0 :
                break

        title_result = title[start_index:end_index]
        return title_result, episode_result



def get_index_m3u8_url(ps):
    index_m3u8_url_result = []
    for paragraph in ps:
        if paragraph.text.find("index.m3u8") != -1:
            var = paragraph.text.replace("\\", "").replace("\n", "").replace("\r", "")
            pre_suf_fix_lib = [('https://', '/index.m3u8')]
            start_index = 0
            end_index = -1

            for prefix, suffix in pre_suf_fix_lib:
                try:
                    start_index = var.find(f'{prefix}')

                except Exception as e:
                    pass
                try:
                    end_index = var.find(f'{suffix}') + len(f"{suffix}")

                except Exception as e:
                    pass
                if start_index != 0 and end_index != -1:
                    index_m3u8_url_result.append(var[start_index:end_index].replace("\\\\", ""))
                    break  # 找到后跳出循环

    return index_m3u8_url_result[0]

def find_download_address():
    pid = os.getpid()


    with open(f"Log/{pid}/downloadPath.txt", "r", errors='ignore', encoding="utf-8") as dp:
        root = dp.read().rstrip("/")

    with open(f"Log/{pid}/src.txt", "r", errors='ignore', encoding="utf-8") as src:
        src1 = src.read()
        print(f"当前解析的HTML文件为: {src1}")
    try:
        with open(src1, "r", errors='ignore', encoding="utf-8") as src11:
            src12 = src11.read()
            title, episode = get_name_and_episode(src1)
            with open(f"Log/{pid}/dst.txt", "w", errors='ignore', encoding="utf-8") as dst:
                dst.write(f"{root}/未完成/{title}/{episode}/")
                if not os.path.exists(f"{root}/{title}"):
                    os.makedirs(f"{root}/{title}", exist_ok=True)
                if not os.path.exists(f"{root}/未完成/{title}/{episode}"):
                    os.makedirs(f"{root}/未完成/{title}/{episode}", exist_ok=True)

            soup = BeautifulSoup(src12, 'html.parser')
            # 如果找到匹配项，则提取其中的 URL
            paragraphs = soup.find_all('script')
            index_m3u8_url = get_index_m3u8_url(paragraphs)
            print(f"解析出的index.m3u8文件地址:{index_m3u8_url}")

            if index_m3u8_url:
                # 下载index.m3u8文件
                print("开始下载m3u8文件...")
                index_m3u8_response = requests.get(index_m3u8_url.rstrip("\n"))
                if index_m3u8_response.status_code == 200:
                    print("开始解析index.m3u8文件...")
                    index_m3u8_content = index_m3u8_response.text

                    with open(f"Log/{pid}/index_m3u8.txt", "w+") as im1:
                        im1.write(index_m3u8_content)

                    with open(f"Log/{pid}/index_m3u8.txt", "r") as im2:
                        while True:
                            line = im2.readline()
                            count = 0
                            if not line:
                                break
                            # 如果行不以'#'开头，且不是预播放的m3u8，则写入到批量下载链接-pid.txt文件
                            if line[0] != "#":
                                count = count + 1
                                new_index_m3u8_url = splicing(os.path.dirname(index_m3u8_url), line)
                                with open(f"Log/{pid}/批量下载链接.txt", "w+") as fileHandler2:
                                    line2 = splicing(os.path.dirname(new_index_m3u8_url), line)
                                    fileHandler2.write(line2)
                                if count == 1:
                                    new_index_m3u8_response = requests.get(new_index_m3u8_url.rstrip("\n"))
                                    if new_index_m3u8_response.status_code == 200:
                                        new_index_m3u8_content = new_index_m3u8_response.text

                                        with open(f"Log/{pid}/index_m3u8-1.txt", "w+") as im3:
                                            im3.write(new_index_m3u8_content)

                                        with open(f"Log/{pid}/index_m3u8-1.txt", "r", ) as im4:
                                            with open(f"Log/{pid}/批量下载链接.txt", "w+") as fileHandler2:
                                                while True:
                                                    # 读取并打印文件中的下一行
                                                    line = im4.readline()
                                                    # 如果行是空的，那么已经到达文件末尾
                                                    if not line:
                                                        break
                                                    # 如果行不以'#'开头，则写入到批量下载链接-pid.txt文件
                                                    if line[0] != "#":
                                                        line3 = splicing(os.path.dirname(new_index_m3u8_url.rstrip("\n")),
                                                                         line)
                                                        fileHandler2.write(line3)
                                    else:
                                        print("抓取m3u8失败", new_index_m3u8_response.status_code)
                        print("获取下载链接完毕.")


                else:
                    print("无法下载index.m3u8文件")
            else:
                print("无法找到index.m3u8文件的URL")
        # else:
        #     print("请求失败")
    except FileNotFoundError as e:
        print(f"{e}")
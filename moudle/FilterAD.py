# coding=utf-8
import os


class DownloadAddress:
    def __init__(self, address_str):
        self.address_str = address_str.replace("\n", "")
        self.list = self.split()
        self.list = self.desuffix()
        self.length = len(self.list)
        self.head = self.list[0] if self.list else ''
        self.tail = self.list[-1] if self.list else ''
        self.isrepeat = self.isrepeat()

    def split(self):
        return self.address_str.split("/")

    def desuffix(self):
        var1 = self.list.pop(-1)
        var2 = var1.split(".")
        var3 = var2[0]
        self.list.append(var3)
        return self.list

    def isrepeat(self):
        return any(self.list.count(char) > 1 for char in set(self.list))


def length_filter(addresses):
    list_lengths = [address.length for address in addresses]
    count_dict = {}
    for item in list_lengths:
        count_dict[item] = count_dict.get(item, 0) + 1

    max_count = max(count_dict.values())
    most_frequent_length = [length for length, count in count_dict.items() if count == max_count]

    # 移除不是出现次数最多的长度的地址
    addresses_to_remove = [address for address in addresses if address.length not in most_frequent_length]
    for address in addresses_to_remove:
        addresses.remove(address)

def name_length_filter(addresses):
    name_lengths = [len(address.tail) for address in addresses]
    count_dict = {}
    for item in name_lengths:
        count_dict[item] = count_dict.get(item, 0) + 1

    max_count = max(count_dict.values())
    most_frequent_length = [length for length, count in count_dict.items() if count == max_count]

    # 移除不是出现次数最多的长度的地址
    addresses_to_remove = [address for address in addresses if len(address.tail) not in most_frequent_length]
    for address in addresses_to_remove:
        addresses.remove(address)


def size_date_filter(addresses):
    dir_list = [os.path.dirname(address.address_str) for address in addresses]
    count_dict = {}
    for item in dir_list:
        count_dict[item] = count_dict.get(item, 0) + 1

    max_count = max(count_dict.values())
    most_frequent_dir = [dir for dir, count in count_dict.items() if count == max_count]

    # 移除不是出现次数最多的路径的地址
    addresses_to_remove = [address for address in addresses if
                           os.path.dirname(address.address_str) not in most_frequent_dir]
    for address in addresses_to_remove:
        print(address.address_str)
        addresses.remove(address)


def repeat_filter(addresses):
    addresses_to_remove = [address for address in addresses if address.isrepeat]
    for address in addresses_to_remove:
        print(address.address_str)
        addresses.remove(address)




def check_and_release_file(file_path):
    try:
        file = open(file_path, "r")
        # 对文件进行操作
        file.close()
    except IOError:
        print(f"文件 {file_path} 可能被占用")
    else:
        print(f"文件 {file_path} 未被占用")





def filter_ad():
    pid = os.getpid()
    with open(f"Log/{pid}/批量下载链接.txt", "r", encoding="utf-8") as f:
        address_list = f.readlines()
        address_list = list(map(DownloadAddress, address_list))

    try:
        with open(f"Log/{pid}/下载链接(filtered).txt", "w", ) as filter:
            print("开始过滤下载链接中广告链接...")
            l1 = len(address_list)
            length_filter(address_list)
            repeat_filter(address_list)
            size_date_filter(address_list)
            name_length_filter(address_list)
            for address in address_list:
                message = address.address_str + "\n"
                filter.write(message)
            l2=len(address_list)
            print(f"下载链接中广告链接过滤完毕. 共过滤{l1-l2}条广告链接.")
    except Exception as e:
        print(f"发生错误：{e}")


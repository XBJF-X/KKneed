    用前须知：
        1.MainGUI.py是带图形界面的脚本，不需要自己设定html文件夹位置，只需要设定下载目标位置就可以了，不能同时投入多个html文件
        2.MainWithoutGUI.py是具有文件监听功能的不带图形界面的脚本，需要自己设定监听哪个文件夹（srcPath），以及下载的目标位置




*********
                    使用前需要做的（如果不配置的话很可能出错）
    1.需要修改想要下载到的目标位置（Main.py里的downloadPath）
    2.需要自己根据网站网页名修改FindDoenloadAddress.py中get_name_and_episode()函数的筛选规则
    具体位置是get_name_and_episode()函数的pre_suf_fix_lib=[("prefix","suffix")]
    其中prefix表示前缀，假如你下载的是番剧，网页标签页标题中，你的番剧名前面有几个字是固定不变的，就填到这里，
    (比如视频名称前后的固定字符串和集数前后的固定字符串，否则可能会出现命名错误)
    3.选择自己想要使用的进程模式，单进程和多进程，其中单进程对网络要求小，多进程对网络和内存要求都要大一些
    默认GUI是多进程，无GUI版是单进程，如果想要修改只需要在其对应py文件下把进程启动后的While循环按照要求注释掉即可
*********
    第一步，创建一个文件夹，把浏览器保存网页（快捷键Ctrl+S）到这个文件夹里
    第二步，运行Main.py
    第三步，把html文件拖进运行产生的窗口
*********
    Tips：
        可以同时处理多个HTML文件，因为已经做了多进程改造,支持下到一半崩溃续下
        如果在下载到合并这一阶段出现问题，重新拖放html到左侧”完整的解析流程“即可
        如果在重命名和移动这一阶段出现问题，重新拖放html到右侧”仅重命名和移动“即可
*********
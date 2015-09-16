# DirScan

##需求
   python 2.x
   requests

一些智能错误关键字判断 和网站域名备份文件

希望多提意见:)

    croxy@Dell:~/PycharmProjects/DirScan$ python dirscan.py 
    Usage: dirscan.py [options] target
    Options:
       -h, --help            show this help message and exit
       -t THREADS_NUM, --threads=THREADS_NUM
                        Number of threads. default = 10
       -e EXT, --ext=EXT     You want to Scan WebScript. default is php
       
##New

1.增加批量扫描 把目标导入target.txt 然后自己改一下Dirscan2.py最后的ext='php'定义后缀就行

2. 添加错误判断如果文件返回长度为0就算不存在:( 不科学的判断方法等待改善

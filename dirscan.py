#__author__ = 'croxy'
# -*- coding: UTF-8 -*-
#!/usr/bin/python

import requests
import optparse
import sys
import threading
import time
import Queue
import re
import difflib

header = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
'Accept-Encoding': 'gzip, deflate, compress',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
"Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"
}


class DirScan:
    def __init__(self, target, threads_num, ext):
        self.target = target.strip()
        self.threads_num = threads_num
        self.ext = ext
        self.lock = threading.Lock()
        #outfile
        self.__load_dir_dict()
        self._getbak()
        self._errorpage()
        self.errorpage = r'信息提示|参数错误|no exists|User home page for|可疑输入拦截|D盾|安全狗|无法加载模块|[nN]ot [fF]ound|不存在|未找到|Error|Welcome to nginx!|404'
        self.regex = re.compile(self.errorpage)

    def _errorpage(self):
        global errtext
        target = self.target
        url = target+'/16fc8a432f7f46853240e38aff9fd8fd.html'
        try:
            r =requests.get(url, headers=header, timeout=5)
            errtext = r.text
        except Exception,e:
            print e


    def __load_dir_dict(self):
        self.queue = Queue.Queue()
        ext = self.ext
        target = self.target
        with open('mulu.txt') as f:
            for line in f:
                mulu = line.replace('$ext$',ext).strip()
                if mulu:
                    self.queue.put(mulu)

    def _getbak(self):
        self.QUEUE = Queue.Queue()
        target = self.target
        hostuser = target.split('.')
        hostuser = hostuser[len(hostuser)-2]
        bak =  ['/'+hostuser+'.rar','/'+hostuser+'.zip','/'+hostuser+hostuser+'.rar','/'+hostuser+'.rar','/'+hostuser+'.tar.gz','/'+hostuser+'.tar','/'+hostuser+'123.zip','/'+hostuser+'123.tar.gz','/'+hostuser+hostuser+'.zip','/'+hostuser+hostuser+'.tar.gz','/'+hostuser+hostuser+'.tar','/'+hostuser+'.bak']
        for j in range(len(bak)):
            BAK = bak[j]
            self.QUEUE.put(BAK)
        with open('bak.txt') as f:
            for line in f:
                baks = line.strip()
                if baks:
                    self.QUEUE.put(baks)

    def _runbak(self):
        try:
            while self.QUEUE.qsize() > 0:
                subs = self.QUEUE.get(timeout=1.0)
                domains = self.target + subs
                #print domains
                try:
                    q = requests.head(domains, headers = header, allow_redirects=False, timeout=5)
                    if q.status_code == 200:
                        print "[*] %s =============> 200" % domains
                except Exception,e:
                    pass
        except Exception,e:
            print e

    def _scan(self):
        #print "[*]%s Scaning...." % self.target
        try:
            while self.queue.qsize() > 0:
                sub = self.queue.get(timeout=1.0)
        #try:
                #print sub
                domain = self.target + sub
                print domain
                r = requests.get(domain, headers = header, timeout=5)
                code = r.status_code
                text = r.text
                #print errtext
                ratios = dict((_, difflib.SequenceMatcher(None, text, errtext).quick_ratio()) for _ in (True, False))
                is404 = all(ratios.values()) and ratios[True] > 0.9
                #print is404
                if code == 200 and not self.regex.findall(text) and not is404:
                    try:
                        title = re.findall(r"<title>(.+?)</title>",text)
                        print "[*] %s =======> 200 (Title:%s)\n" %(domain, title[0]),
                    except Exception,e:
                        print "[*] %s =======> 200\n" %domain,

        except Exception,e:
            pass


    def run(self):
        self.start_time = time.time()
        for i in range(self.threads_num):
            q = threading.Thread(target=self._runbak, name=str(i))
            q.start()
            t = threading.Thread(target=self._scan, name=str(i))
            t.start()


if __name__ == '__main__':
    parser = optparse.OptionParser('usage: %prog [options] http://www.c-chicken.cc')
    parser.add_option('-t', '--threads', dest='threads_num',
              default=10, type='int',
              help='Number of threads. default = 10')
    parser.add_option('-e', '--ext', dest='ext', default='php',
               type='string', help='You want to Scan WebScript. default is php')
   # parser.add_option('-o', '--output', dest='output', default=None,
   #          type='string', help='Output file name. default is {target}.txt')

    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(0)

    d = DirScan(target=args[0],threads_num=options.threads_num,ext=options.ext)
    d.run()

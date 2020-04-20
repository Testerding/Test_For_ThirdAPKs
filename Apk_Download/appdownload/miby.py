#coding=utf-8
import logging
import requests
import re
import urllib
import sys
import socket
sys.path.append("..")
from utils.utils import PhoneUtil
from bs4 import BeautifulSoup
socket.setdefaulttimeout(30)

_root_url="http://app.mi.com"

class MiBy:
    '''
    小米包名下载
    '''
    def __init__(self):
        logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='..\\log\\runtime.log',
        filemode='a+'
      )
        self.logger = logging.getLogger()
       
    def getAppPages(self):
        '''
        获取包名下载地址
        '''
        app_lists = self.getAppList()
        app_pages=[]
        for appname in app_lists:
            app_page = "http://app.mi.com/details?id="+appname+"&ref=search"  #Mi商店搜索下载规则
            app_pages.append(app_page)
        #print (app_pages)
        return app_pages


    def getAppList(self):
        '''
        获取配置文件内包名列表
        '''
        app_lists=[]
        apptxt = open("..\\config\\mi.txt",'r')
        line = apptxt.readline()
        while line:
            if len(line) > 0:
                line = line.strip("\n")
                app_lists.append(line)
            line=apptxt.readline()
        apptxt.close()
        return app_lists

    def getDownLoadUrl(self,path="..\\apk\\"):
        '''
        获取下载地址并进行下载
        '''
        data = PhoneUtil.getTodayData(self)
        apk_address=path+'MiByName'+data+"\\"
        PhoneUtil.checkAndCreatFolder(self,apk_address)
        urls = self.getAppPages()
        for url in urls:
            wbdata = requests.get(url).text
            soup=BeautifulSoup(wbdata,"html.parser")
            try:
                download_link=soup.find(class_="download")["href"]
                download_url=urllib.parse.urljoin(_root_url, str(download_link))
                packagename = ((download_url.split('='))[1]).split('&')[0]
                self.logger.info("正在下载应用: "+packagename)
                print("正在下载应用: "+packagename)
                self.auto_down(download_url,apk_address+packagename+'.apk')
            except Exception as e:
                print("异常app网页"+str(url))
                self.logger.info("异常app网页"+str(url) + str(e))


    def auto_down(self,url,filename):
        '''
        尝试下载5次
        '''
        try:
            urllib.request.urlretrieve(url,filename)
            #下载完整包后才会加载下载完成log
            print("下载完成: "+filename.split("\\")[-1])
            self.logger.info("下载完成: "+filename.split("\\")[-1])
        except (socket.timeout,Exception) as e:
            #重试5次
            count = 1
            while count <= 5:
                try:
                    urllib.request.urlretrieve(url,filename)
                except (socket.timeout,Exception):
                    count += 1
            if count > 5:
                print("应用下载5次失败："+filename)
                self.logger.info("应用下载5次失败："+filename)


if __name__=="__main__":
    MiBy=MiBy()
    MiBy.getDownLoadUrl()
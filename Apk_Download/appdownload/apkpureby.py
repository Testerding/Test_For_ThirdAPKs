#coding=utf-8
import logging
import requests
import re
import urllib
import sys
import socket
sys.path.append("..")
socket.setdefaulttimeout(30)
from utils.utils import PhoneUtil
from bs4 import BeautifulSoup

_root_url="https://apkpure.com" #/cn/search?q=com.android.vending

class ApkPureBy:
    '''
    APK Pure 通过包名下载
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
        self.header= {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}
       
    def getAppPages(self):
        '''
        获取单个搜索apk的页面
        '''
        app_lists = self.getAppList()
        app_pages=[]
        for appname in app_lists:
            app_page = "https://apkpure.com/cn/search?q="+appname  #Mi商店搜索下载规则
            app_pages.append(app_page)
        return app_pages


    def getAppList(self):
        '''
        获取配置文件中的APP名称
        '''
        app_lists=[]
        apptxt = open("..\\config\\apkpure.txt",'r')
        line = apptxt.readline()
        while line:
            if len(line) > 0:
                line = line.strip("\n")
                app_lists.append(line)
            line=apptxt.readline()
        apptxt.close()
        return app_lists

    def getAllName(self):
        '''
        获取配置文件中的APP名称
        '''
        app_names=''
        apptxt = open("..\\config\\apkpure.txt",'r')
        line = apptxt.readline()
        while line:
            if len(line) > 0:
                line = line.strip("\n")
                app_names = app_names + line+"#"
            line=apptxt.readline()
        apptxt.close()
        return app_names


    def getDownLoadUrl(self,path="..\\apk\\"):
        '''
        获取app的下载地址
        '''
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36')]
        urllib.request.install_opener(opener)
        data = PhoneUtil.getTodayData(self)
        apk_address=path+'ApkPureByName'+data+"\\"
        PhoneUtil.checkAndCreatFolder(self,apk_address)
        urls = self.getAppPages()
        app_names = self.getAllName()
        for url in urls:
            wbdata = requests.get(url,self.header).text
            soup=BeautifulSoup(wbdata,"html.parser")
            try:
                download_link=soup.find(class_="more-down")["href"]
                download_url=urllib.parse.urljoin(_root_url, str(download_link))
                packagename = (download_link.split('/'))[3]
                index_app = urls.index(url) 
                except_app =app_names.split("#")[index_app]
                if not packagename in app_names:
                    index_app = urls.index(url) 
                    print("apkpure无对应app:"+except_app)
                    self.logger.info("apkpure no app："+except_app)
                    continue
                downurl_data=requests.get(download_url,self.header).text
                soup2=BeautifulSoup(downurl_data,"html.parser")
                download_link_page=soup2.find(class_=" da")["href"]
                download_page=urllib.parse.urljoin(_root_url, str(download_link_page))
                app_data=download_page+'/download?from=details'
                detail_data = requests.get(app_data, headers=self.header).text
                soup3=BeautifulSoup(detail_data,"html.parser")
                download=soup3.find(id="download_link")["href"]
                self.auto_down(download,apk_address+packagename+'.apk')
            except:
                self.logger.info("异常app网页/网络异常"+str(packagename))


    def auto_down(self,url,filename):
        '''
        尝试下载5次
        '''
        try:
            print("正在下载: "+filename.split("\\")[-1])
            self.logger.info("正在下载: "+filename.split("\\")[-1])
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
    ApkPureBy=ApkPureBy()
    ApkPureBy.getDownLoadUrl()
#coding=utf-8
import re
import sys
import time
import urllib
import logging
import requests
from bs4 import BeautifulSoup
sys.path.append("..")
from utils.utils import PhoneUtil


class MiDownload:
    '''
    小米下载工具
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

    def parser_apks(self,count=10):
        '''
        小米应用市场
        返回的是一个map  下载名称以及对应的下载地址
        @count 是下载个数
        '''
        _root_url="http://app.mi.com"
        res_parser={}
        page_num=1
        while count:
            wbdata = requests.get("http://app.mi.com/topList?page="+str(page_num)).text
            soup=BeautifulSoup(wbdata,"html.parser")
            links=soup.find_all('h5')
            for link in links:
                if "/details?" in str(link):
                    time.sleep(0.5)
                    link=(str(link).split('"'))[1]
                    detail_link=urllib.parse.urljoin(_root_url, link)
                    package_name=detail_link.split("=")[1]
                    download_page=requests.get(detail_link).text
                    soup1=BeautifulSoup(download_page,"html.parser")
                    try:
                        download_link=soup1.find(class_="download")["href"]
                        download_url=urllib.parse.urljoin(_root_url, str(download_link))
                    except:
                        self.logger.info("异常app网页"+str(package_name))
                    if download_url not in res_parser.values():
                        res_parser[package_name]=download_url
                        info=open('..\\config\\mi_apk_info.txt','a')
                        info.write(package_name+'    '+res_parser[package_name]+"\n")
                        info.close()
                        count=count-1
                    if count==0:
                        break
            if count >0:
                page_num=page_num+1
        return res_parser


    def craw_apks(self,count=10, path="..\\apk\\"):
        '''
        爬取方法
        在获取的map里面循环下载apk
        每次失败/连接超时  重新获取5次
        '''
        data=PhoneUtil.getTodayData(self)
        apk_address=path+'MiTop'+data+"\\"
        PhoneUtil.checkAndCreatFolder(self,apk_address)
        res_dic=self.parser_apks(count)
        record=open('..\\log\\mi_undown_apk_info.txt','a')
        record.write("*********************"+data)
        record.close()
        print(("爬取apk数量为: "+str(len(res_dic))))
        self.logger.info("爬取apk数量为: "+str(len(res_dic)))
        for apk in res_dic.keys():
            print ("正在下载应用: "+apk)
            self.logger.info("正在下载应用: "+apk)
            try:
                self.auto_down(res_dic[apk],apk_address+apk+".apk")
            except Exception as e:
                #mi应用市场bug，有些页面无下载链接
                self.logger.info("网络问题/网页异常,下载失败"+apk)
                self.logger.info("报错信息为"+str(e))

    def auto_down(self,url,filename):
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
                except (socket.timeout,Exception) as e:
                    count += 1
            if count > 5:
                print("应用下载5次失败："+filename)
                undownload_info=open('..\\log\\mi_undown_apk_info.txt','a')
                undownload_info.write(filename.split("\\")[-1]+"\n")
                self.logger.info("应用下载5次失败："+filename+str(e))
if __name__=="__main__":
    MiBy=MiDownload()
    MiBy.craw_apks(1)



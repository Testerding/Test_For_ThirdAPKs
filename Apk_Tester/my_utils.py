#coding=utf-8
import os
import datetime
import configparser

"""
Created on 2020年04月01日

@author: panda
"""


class MyUtil:
	def checkAndCreatFolder(self,folder_name):
		if os.path.exists(folder_name):
			pass
		else:
			os.makedirs(folder_name)

	def getTodayData(self):
		data = str(datetime.datetime.now()).replace("-","_").replace(" ","_").replace(".","_").replace(":","_")
		return data

	def getFiles(self,path='apk',file_type='txt'):
		need_files=[] 
		for root, dirs, files in os.walk(path): 
			for file in files: 
				if os.path.splitext(file)[1] == '.'+file_type:
					need_files.append(os.path.join(root, file))
		return need_files


class ConfigReader:
	'''
	配置文件类
	'''
	def __init__(self):
		'''初始化配置文件类'''
		self.conf= configparser.ConfigParser()
		
	def readConf(self,type,info):
		'''读取配置文件'''
		self.conf.read('test.conf',encoding="utf-8-sig")  # 文件路径
		name = self.conf.get(type, info)  # 获取指定section 的option值
		return name

	def getLists(self,type,info):
		'''获取列表规则'''
		lists = []
		self.conf.read('test.conf',encoding="utf-8-sig")  # 文件路径
		values = str(self.conf.get(type, info))  # 获取指定section 的option值
		lists = values.split(" ")
		return lists




if __name__=='__main__':
	MyUtil=MyUtil()
	MyUtil.getFiles(file_type='py')
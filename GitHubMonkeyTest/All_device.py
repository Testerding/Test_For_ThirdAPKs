# -*- coding: GB2312 -*-
import os
import os.path
import time
import glob

# ɾ�����в���cmd�ű�
path = "D:\\PyCharm\\monkeyTest-master\\"
for file in glob.glob(os.path.join(path, '*.cmd')):
    os.remove(file)

os.system("cls")  # os.system("cls")������������
rt = os.popen('adb devices').readlines()  # os.popen()ִ��ϵͳ�������ִ�к�Ľ��
#print(rt)
n = len(rt) - 2
print("��ǰ�����Ӵ����ֻ���Ϊ��" + str(n))
aw = input("�Ƿ�Ҫ��ʼ���monkey���ԣ�������(y or n): ")
run_time =time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

if aw == 'y':
    print("monkey���Լ�����ʼ....")
    #count = input("��������Ҫ���е�monkey���Դ���: ")
    #testmodel = input("����������Ҫ���е��β��Ի��Ƕ���������ԣ�������(1-�����β��ԣ�2-��������������): ")
    ds = range(n)
    for i in range(n):
        nPos = rt[i + 1].index("\t")
        #print(nPos)
        dev = rt[i + 1][:nPos]
        #print(dev)
        promodel = os.popen("adb -s " + dev + ' shell cat /system/build.prop | find "ro.product.model="').readlines()  # ��ȡ�ֻ��ͺ�
        modelname = promodel[0]  # ��list��ȡ����һ��ֵ
        model = modelname[17:].strip('\r\n')
        proname = os.popen("adb -s " + dev + ' shell cat /system/build.prop | find "ro.product.brand="').readlines()  # ��ȡ�ֻ�����
        roname = proname[0]
        name = roname[17:].strip('\r\n')
        packagename = os.popen("adb -s " + dev + ' shell pm list packages | find "com.quvideo.slideplus"').readlines() #��ȡpackage����
        package = packagename[0]
        pk = package[8:].strip('\r\n')
        if pk == 'com.quvideo.slideplus':
            """filedir = os.path.exists("D:\\PyCharm\\monkeyTest-master\\")
            if filedir:
                print("File Exist,go on testing!")
            else:
                os.mkdir("D:\\PyCharm\\monkeyTest-master\\")"""
            devicedir = os.path.exists("D:\\PyCharm\\monkeyTest-master\\" + name + '-' + model + '-' + dev)
            if devicedir:
                print("File Exist, go on testing!")
            else:
                os.mkdir("D:\\PyCharm\\monkeyTest-master\\" + name + '-' + model + '-' + dev)  # ���豸ID������־Ŀ¼�ļ���
            wl = open("D:\\PyCharm\\monkeyTest-master\\" + name + '-' + model + '-' + dev + '-logcat' + '.cmd', 'w')
            wl.write('adb -s ' + dev + ' logcat' + ' > D:\\PyCharm\\monkeyTest-master\\' + '"' + name + '-' + model + '-' + dev + '"' + '\\'+ run_time + '_logcat.txt\n' )
            #wl.write(' > D:\\PyCharm\\monkeyTest-master\\' + '"' + name + '-' + model + '-' + dev + '"' + '\\logcat.txt\n')
            wl.close()
            #if testmodel == '1':
            wd = open("D:\\PyCharm\\monkeyTest-master\\" + name + '-' + model + '-' + dev + '-device' + '.cmd', 'w')
            wd.write(
                'adb -s ' + dev + ' shell monkey -p com.quvideo.slideplus -s 200 --throttle 500 --ignore-crashes --ignore-timeouts --pct-touch 45 --pct-trackball 15 --pct-appswitch 10 --pct-syskeys 10 --pct-motion 20 -v -v 1000 ')  # ѡ���豸ִ��monkey
            wd.write('> D:\\PyCharm\\monkeyTest-master\\' + '"' + name + '-' + model + '-' + dev + '"' + '\\' + run_time + '_monkey.txt\n')
            wd.write('������ɣ���鿴��־�ļ�~')
            wd.close()
            """elif testmodel == '2':
                wd = open("D:\\PyCharm\\monkeyTest-master\\" + name + '-' + model + '-' + dev + '-device' + '.cmd', 'w')
                wd.write(':loop')
                wd.write('\nset /a num+=1')
                wd.write('\nif "%num%"=="4" goto end')
                wd.write(
                    '\nadb -s ' + dev + ' shell monkey -p com.quvideo.slideplus -s 200 --throttle 500 --ignore-crashes --ignore-timeouts --pct-touch 45 --pct-trackball 15 --pct-appswitch 10 --pct-syskeys 10 --pct-motion 20 -v -v 1000 ')  # ѡ���豸ִ��monkey
                wd.write('> D:\\PyCharm\\monkeyTest-master\\' + '"' + name + '-' + model + '-' + dev + '"' + '\\monkey.txt\n')
                wd.write('@echo ���Գɹ���ɣ���鿴��־�ļ�~')
                wd.write('\nadb -s ' + dev + ' shell am force-stop ' + pk)
                wd.write('\n@ping -n 15 127.1 >nul')
                wd.write('\ngoto loop')
                wd.write('\n:end')
                wd.close()"""
        else:
            print("�����ֻ�" + name + '-' + model + "δ��װСӰ��")

    # ִ���������ɵ�cmd�ű�path='E:\\monkey_test\\'
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) == True:
            if file.find('.cmd') > 0:
                os.system('start ' + os.path.join(path, '"' + file + '"'))  # dos�������ļ�������пո������˫����
                time.sleep(1)
elif aw == 'n':
    print('�û������������ԣ����Խ�����')
else:
    print("���Խ���������Ƿ�������������y or n��")
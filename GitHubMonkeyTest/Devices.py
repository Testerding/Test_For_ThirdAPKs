# -*- coding: GB2312 -*-
import os
import os.path
import time
import glob

# ɾ�����в���cmd�ű�
path = "D:\\PyCharm\\Monkey_performance\\"
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
    for i in range(n):
        nPos = rt[i + 1].index("\t")
        #print(nPos)
        dev = rt[i + 1][:nPos]
        print(dev)
        phone_model = os.popen("adb -s " + dev + ' shell cat /system/build.prop | find "ro.product.model="').readlines()  # ��ȡ�ֻ��ͺ�
        model = phone_model[0][17:].strip('\r\n')
        #print(model)
        phone_name = os.popen("adb -s " + dev + ' shell cat /system/build.prop | find "ro.product.brand="').readlines()  # ��ȡ�ֻ�����
        #roname = phone_name[0]
        name = phone_name[0][17:].strip('\r\n')
        package_name = os.popen("adb -s " + dev + ' shell pm list packages | find "com.quvideo.slideplus"').readlines() #��ȡpackage����
        #package = package_name[0]
        app_name = package_name[0][8:].strip('\r\n')
        path_log = "D:\\PyCharm\\Monkey_performance\\" + name + '-' + model
        if app_name == 'com.quvideo.slideplus':
            device_dir = os.path.exists(path_log)
            if device_dir:
                print("File Exist, go on testing!")
            else:
                os.mkdir(path_log)  # ���豸ID������־Ŀ¼�ļ���
            """w_log = open(path_log + '-logcat' + '.cmd', 'w')
            w_log.write('adb -s ' + dev + ' logcat -v time > ' + '"' + path_log + '"' + '\\'+ run_time + '_logcat.txt\n' )
            w_log.close()"""

            w_adb = open(path_log + '-device' + '.cmd', 'w')
            w_adb.write(
                'adb -s ' + dev + ' shell monkey -p ' + app_name + ' -s 200 --throttle 500 --ignore-crashes --ignore-timeouts --pct-touch 45 --pct-trackball 15 --pct-appswitch 10 --pct-syskeys 10 --pct-motion 20 -v -v 1000 > ')  # ѡ���豸ִ��monkey
            w_adb.write('"' + path_log + '"' + '\\' + run_time + '_monkey.txt\n')
            #wd.write('������ɣ���鿴��־�ļ�!')
            w_adb.close()

        else:
            print("�����ֻ�" + name + '-' + model + "δ��װСӰ��")

    # ִ���������ɵ�cmd�ű�'

    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) == True:
            if file.find('.cmd') > 0:
                os.system('start ' + os.path.join(path, '"' + file + '"'))  # dos�������ļ�������пո������˫����
                time.sleep(1)
elif aw == 'n':
    print('�û������������ԣ����Խ�����')
else:
    print("���Խ���������Ƿ�������������y or n��")
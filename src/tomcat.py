#!/usr/bin/python3
# 文件名: using_sys.py

import requests
import datetime
import time
import os,fnmatch
import subprocess
from glob import glob
import re
import sys
import platform
from apscheduler.schedulers import Scheduler

# 发送带附件的邮件需要引入的模块
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

# 文件路径夹
filePath = "D:\\app_server\\sxt_server\\bin\\"
#filePath = "E:\\tomcat1\\bin\\"
# tomcat的启动路径
tomcatStart = filePath + "startup.bat"
# tomcat的关闭路径
tomcatStop = filePath + "shutdown.bat"
# 要检查的url
#url = "http://127.0.0.1:8080/sxt/ph/ph_login.jsp"
url = "http://sxt.xiaotq.cn/sxt/ph/ph_login.jsp"

#dbsync路径
dbsyncPath = "D:\\dbsync\\sxt_dbsync_client.exe"

# 正则查找某文件
word = "hs_err_pid*.log;"

#查找某文件
def all_files(root, patterns='*', single_level=False, yield_folder=False):
    # 将模式从字符串中取出放入列表中
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folder:
            files.extend(subdirs)
        files.sort()
        for fname in files:
            for pt in patterns:
                if fnmatch.fnmatch(fname, pt):
                    yield os.path.join(path, fname)
                    break
        if single_level:
            break

def get_recentError_file():
    # fnmatch 来检查文件名匹配模式
    # os.path fnmatch os.walk 生成器
    thefile=list(all_files(filePath, word))
    if len(thefile) > 0:
        #对文件修改时间进行升序排列
        thefile.sort(key=lambda fn:os.path.getmtime(fn))
        #获取最新修改时间的文件
        filetime = datetime.datetime.fromtimestamp(os.path.getmtime(thefile[-1]))
        #获取文件所在目录
        filepath = os.path.join(filePath,thefile[-1])
        print("最新修改的文件(夹)："+thefile[-1])
        print("时间："+filetime.strftime('%Y-%m-%d %H-%M-%S'))
        return filepath
    else:
        return ''

my_sender='793514387@qq.com'    # 发件人邮箱账号
my_pass = 'bdbrmjidydiybahg'    # 发件人邮箱密码
my_user='793514387@qq.com'      # 收件人邮箱账号，我这边发送给自己

def getNowDate():
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return nowTime

def mail():
    ret=True
    try:
        fileName = get_recentError_file()
        mail_msg = "<p>应用访问出现异常...</p><p><a href='"+url+"'>点击手动验证</a></p>"
        if len(fileName) > 0:
            print("============发送带附件的文件=============")
            msg = MIMEMultipart()
            # 邮件正文内容
            msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))
            # 构造附件1，传送当前目录下的 test.txt 文件
            att1 = MIMEText(open(get_recentError_file(), 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att1["Content-Disposition"] = 'attachment; filename="error.log"'
            msg.attach(att1)

            msg['From']=formataddr(["三信通智能小三",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=formataddr(["天震",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject']="服务器监控异常"+ getNowDate()    # 邮件的主题，也可以说是标题
        
            server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        else:
            print("============发送没带附件的文件=============")
            msg = MIMEText(mail_msg, 'html', 'utf-8')
            msg['From']=formataddr(["三信通智能小三",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=formataddr(["天震",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject']="服务器监控异常"+ getNowDate()    # 邮件的主题，也可以说是标题
        
            server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接        
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret
 
# 启动tomcat
def startTomcat():
    subprocess.Popen(tomcatStart)

# 关闭tomcat
def stopTomcat():
    subprocess.Popen(tomcatStop)
    # 终止tomcat进程，如果系统只有一个tomcat在运行，没其他的Java程序在跑的话，用这个可以快速关掉进程，该方式是在上面这种情况还关闭不了的情况下使用的
    # os.system("taskkill /F /IM java.exe")

def startDBsync():
    try:
        _p = subprocess.Popen(dbsyncPath)
        time.sleep(4)
        print("sxt_dbsync_client:"+str(datetime.datetime.now())+"PID:"+str(_p.pid))
        return 1
    except:
        print("异常")
        retun -1

def stopDBsync():
    os.system("taskkill /F /IM sxt_dbsync_client.exe")
    time.sleep(4)

schedudler = Scheduler(daemonic = False)    
 
@schedudler.cron_schedule(second='*',id='my-job', day_of_week='0-6', hour='9-12,22-23')    
def quote_send_sh_job():
    flag = startDBsync()
    if flag == -1:
        schedudler.remove_job(my-job)
    print ("a simple cron job start at"+str(datetime.datetime.now()))    
    
schedudler.start()       

 # 检查系统是否还存活 true 还存活， false 已经关闭
def checkWeb():
    i = 0
    for i in range(3):
        try:
            i = i + 1
            result = True
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
                }
            response = requests.get(url, timeout = 10) #请求超时时间为10秒
            # encode = response.encoding #从http header 中猜测的相应内容编码方式
            code = response.status_code #http请求的返回状态，若为200则表示请求成功,返回的状态码是 int类型
            print(str(getDate()) + "  检测到状态编码：" + str(code))
            if code == 200:
                result = True
            else:
                result = False
            time.sleep(5) #休眠5秒
        except:
            result = False
    return result

# 获取时间
def getDate():
    today = datetime.date.today()
    return today

"""
根据端口获取PID
    返回获取的PID
"""
def getPID(port):
    try:
        # 根据命令获取到指定端口的信息 TCP    0.0.0.0:8080（端口）           0.0.0.0:0              LISTENING       6856（PID）
        ret = os.popen("netstat -nao | findstr " + port)
        str_list = ret.read()
        print(str_list)
        # 字符串按空格分成列表split()
        ret_list = str_list.split()
        # 截取出pid
        pid = ret_list[4][:6]
        print(type(pid))
        return pid
    except:
        print("根据端口找不到该对应应用")
        return "0"

"""
# 根据PID杀死进程
"""
def kill(pid):
    try:
        os.popen('taskkill.exe /pid:' + str(pid))
        print("已经杀死PID为 " + pid + " 的进程")
    except OSError:
        print('没有如此进程!!!')
        errorStr = OSError.errno
        print("错误信息" + errorStr)

"""
if __name__ == '__main__':
    pid = getPID("8080")
    print(pid)
    if pid == "0":
        print("没有需要删除的进程")
    else:
        kill(pid)
"""
def mainApp():
    while True:
        print(str(getDate()) + " =========开始检测系统状态=============")
        if checkWeb() == False:
            print(str(getDate()) + "  系统异常中·············")
            print("=====开始停止tomcat，等待15秒··====")
            stopTomcat()
            print("=====开始发送邮件··====")
            ret=mail()
            if ret:
                print("邮件发送成功")
            else:
                print("邮件发送失败")
            time.sleep(10)  # 休眠15秒来关闭应用,系统应用在服务器上关闭有点慢
            print("=====正在重启tomcat====")
            startTomcat()
        else:
            print(str(getDate()) + "  ***系统正常***")

        
        print(str(getDate()) + "  =========结束检测系统状态=============")
        print(str(getDate()) + " =========开始检测数据库同步工具状态=============")

        print(str(getDate()) + " =========结束检测数据库同步工具状态=============")
        time.sleep(30)  # 休眠3分钟

mainApp()



#!/usr/bin/python3
# 文件名: config.py
import configparser
import os

class Config:

    def __init__(self, filePath=None):
        if filePath:
            configPath = filePath
        else:
            root_dir = os.path.dirname(os.path.abspath('.'))  # 获取当前文件所在目录的上一级目录，即项目所在目录
            configPath = root_dir+"/src/config.ini"
        self.configparser = configparser.ConfigParser()
        self.configparser.read(configPath, "utf-8")

    def get_cpu(self, param):
        value = self.configparser.get("cpu", param)
        return value

    def get_web(self, param):
        value = self.configparser.get("web", param)
        return value

    def get_email(self, param):
        value = self.configparser.get("email", param)
        return value

if __name__ == '__main__':
    test = Config()
    t = test.get_cpu("isemail")
    print(t)


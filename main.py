# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from requests.api import get
from Ui_novel import Ui_NovelGet
import win32api,win32con

from soupsieve import select
from w3lib.html import remove_tags
import requests
from bs4 import BeautifulSoup
import re


class MyMainForm(QMainWindow, Ui_NovelGet):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.start.clicked.connect(self.display)

    def display(self):
        novelurl = str(self.URLget.text())
        try:
            ret = requests.get(url=novelurl)
        except:
            win32api.MessageBox(0, "地址解析错误", "提醒", win32con.MB_ICONWARNING)
        ulrpre = re.match(r'(.*?).com/', novelurl).group(1) + '.com'
        ret.encoding = ret.apparent_encoding
        soup = BeautifulSoup(ret.text, "lxml")
        strhref = str(soup.select('#list'))
        listhref = re.findall(r'<a href="(.*?)">(.*?)</a>', strhref)
        listhrefreal = []
        for chapter_info in listhref:
            chapter_url, chapter_title = chapter_info
            chapter_url = ulrpre + chapter_url
            listhrefreal.append(chapter_url)

        self.IprogressBar.setMaximum(len(listhref))
        file = open('novel.txt', 'w', encoding="utf-8")
        for i in range(len(listhrefreal)):
            ret = requests.get(url=str(listhrefreal[i]))
            ret.encoding = ret.apparent_encoding

            soup = BeautifulSoup(ret.text, "lxml")
            strname = str(soup.select('h1'))
            strname = remove_tags(strname)
            strname = strname.lstrip('[')
            strname = strname.rstrip(']')
            file.write(strname + '\n\n')

            strs = str(soup.select('#content'))
            strs = remove_tags(strs)
            strs = strs.lstrip('[')
            strs = strs.rstrip(']')
            file.write(strs + '\n\n\n\n')
            self.IprogressBar.setValue(i)
        file.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
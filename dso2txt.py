#!/usr/bin/python
# -*- coding: utf-8 -*-
# Проект - Редактор баз данных Форварда
# Автор - Зонов В. М.
# Старт проекта - 26.11.2010
# Лицензия - GPL v 2

# Файл dso2txt.py
# Консольная утилита по конвертации БД в тестовик

# Формат использования:
#
import sys, os, stat, string, dso_tools
#from PyQt4 import QtGui
#from PyQt4 import QtCore
from struct import *


BDFileName="/home/corvin/Programizm/Python/ForwardBD/reports/sut/Repdata.dso"
IniFileName="/home/corvin/Programizm/Python/ForwardBD/reports/sut/RepData.ini"
print BDFileName
print IniFileName

x=dso_tools.ReadIni("xset.ini")
print "\n\n",x
y=dso_tools.CheckDSO("xset.dso",x)
print "\n\n",x
dso_tools.ReadDSO("xset.dso",x,y)


#!/usr/bin/python
# -*- coding: utf-8 -*-
# Проект - Редактор баз данных Форварда
# Автор - Зонов В. М.
# Старт проекта - 26.11.2010
# Лицензия - GPL v 2

# Файл txt2dso.py
# Консольная утилита по конвертации текстовика в БД

# Формат использования:
#
import sys, os, stat, string, dso_tools
#from PyQt4 import QtGui
#from PyQt4 import QtCore
from struct import *



Fields=dso_tools.ReadIni("xset.ini")
#print "\n\n",x

#файл со входными данными, имя выходного файла, данные (кортеж) с данными ReadIni
dso_tools.WriteDSO("DSO_в_тексте","out.dso",Fields)


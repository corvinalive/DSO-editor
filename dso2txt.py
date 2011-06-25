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

import optparse


usage = u"Редактор баз данных Forward.\nРаспаковка данных из файла БД в текстовой файл\nИспользование: %prog [options] имя_dso-файла"
parser = optparse.OptionParser(usage)
parser.add_option("-i", "--ini-file", dest="ini_file", help=u"Имя ini-файла")
parser.add_option("-o", "--output-file", dest="output_file", help=u"Имя выходного файла")

(options, args) = parser.parse_args()

if len(args) < 1:
	parser.error(u"Недостаточно аргументов. Задайте имя dso-файла для распаковки в текстовый файл. Запустите с ключем -h для справки")

inifn=""
if options.ini_file != None:
	inifn = options.ini_file
else:
	inifn=args[0]
	inifn=inifn[0:(len(inifn)-4)]
	inifn+=".ini"

outfn=""
if options.output_file != None:
	outfn = options.output_file
else:
	outfn=args[0]
	outfn=outfn[0:(len(outfn)-4)]
	outfn+=".txt"

#Читаем и и разбираем ini-фалй
x=dso_tools.ReadIni(inifn)

#Проверяем размер записи, кол-во записей
y=dso_tools.CheckDSO(args[0],x)

#Читаем и преобразуем в текст, пишем в текстовый файл
dso_tools.ReadDSO(args[0],x,y,outfn)


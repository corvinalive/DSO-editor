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
import sys, os, stat, string, dso_tools, time
#from PyQt4 import QtGui
#from PyQt4 import QtCore

import optparse


usage = u"Редактор баз данных Forward.\nУпаковка данных из текстового фалй в файл БД.\nИспользование: %prog [options] имя_текстового_файла"
parser = optparse.OptionParser(usage)
parser.add_option("-i", "--ini-file", dest="ini_file", help=u"Имя ini-файла")
parser.add_option("-o", "--output-file", dest="output_file", help=u"Имя выходного файла")

(options, args) = parser.parse_args()

if len(args) < 1:
	parser.error(u"Недостаточно аргументов. Задайте имя текстового файла для упаковки в файл базы данных dso. Запустите с ключем -h для справки")

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
	outfn+=".dso"



#Делаем бэкап перезаписываемого файла, если он есть
t=time.localtime(time.time())
backfn=str(t[0])+" "+string.zfill(str(t[1]),2)+" "+string.zfill(str(t[2]),2)+" "+string.zfill(str(t[3]),2)+string.zfill(str(t[4]),2)+string.zfill(str(t[5]),2)
backfn+=" "
backfn+=outfn

Fields=dso_tools.ReadIni(inifn)

if os.path.exists(outfn):
	os.rename(outfn,backfn)
	print "Была создана резервная копия файла ",outfn, "под именем ", backfn

#файл со входными данными, имя выходного файла, данные (кортеж) с данными ReadIni
dso_tools.WriteDSO(args[0],outfn,Fields)


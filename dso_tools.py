#!/usr/bin/python
# -*- coding: utf-8 -*-
# Проект - Редактор баз данных Форварда
# Автор - Зонов В. М.
# Старт проекта - 26.11.2010
# Лицензия - GPL v 2

# Файл dso_tools.py
# Модуль - стандартные функции по работе с базами данных Форварда

# План работ:
# Предоставляемые функции:
# 1. Чтение формата БД
# 2. 
# 3. 
#

import ConfigParser
import os
import stat
import sys
import string
import struct

#Константы для доступа данным, возращаемым функцией ReadIni кортеж 
readini_fld_type = 0
readini_fld_name = 1
readini_size = 2
readini_unpackstr = 3

#Константы для доступа данным, возращаемым функцией CheckDSO
checkdso_file_size = 0
checkdso_size_record = 1
checkdso_records = 2

#Функция разбора ини-файла
def ReadIni(ini_file_name):
	print "\nФайл dso_tools.py функция ReadIni\n", "\nИмя ini-файла:", ini_file_name

	config = ConfigParser.ConfigParser()
	config.read(ini_file_name)

	if not config.has_section('Fields'):
		print('В ini файле не обнаружена секция "Fields"')
		sys.exit(0)

	FieldCount = config.getint("Fields","Number")
	print "FieldCount=", FieldCount

	if FieldCount <= 0:
		print('В ini количество полей <= 0 (Fields)')
		sys.exit(0)

	Fields =[]
	for i in range(FieldCount):
		s = "Field"+str(i+1)
		fld_type = string.lower(config.get(s,"Type"))
		print s," field_type=",fld_type

		fld_name = config.get(s,"Name")
		print s," field_name=",fld_name

		#сохранение размера поля			
		size=0
		unpackstr=''
		if fld_type == "ftinteger":
			size=4
			unpackstr='=i'
		
		elif fld_type == "ftfloat":
			size=8
			unpackstr='=d'
			
		elif fld_type== "ftstring":
			size=string.atoi(config.get(s,"Size"))
			unpackstr='=s'
			
		else:
			print "Ошибка: not found size of type ", fld_type

		Fields.append((fld_type,fld_name,size, unpackstr))

	print "Fields=\n",Fields
	return Fields

def CheckDSO(DSOFileName, Fields):
	print "\nФайл dso_tools.py функция CheckDSO\n"
	#вычисление размера одной записи
	size_record=0
	for i, item in enumerate(Fields):
		size_record += item[readini_size]
	print "Размер одной записи ", size_record

	#вычисление количества записей
	file_size=os.stat(DSOFileName)[stat.ST_SIZE]
	print "Размер файла БД в байтах:", file_size

	records = file_size/size_record
	kratno = records*size_record - file_size
	if kratno == 0 :
		print "ОК: Размер файла кратен размеру записи. Количество записей ", records
	else:
		print "ОШИБКА: размер файла не кратен размеру записи. Возможно, файл поврежден"
		#sys.exit(0)

	BD_Info = (file_size, size_record, records)

	print "BD_Info=",BD_Info
	return BD_Info

def ReadRecord(DSOFileName, Fields, BD_Info, Index):
	print "\nФайл dso_tools.py функция ReadRecord\n"
	
	print "\nDSOFN = ", DSOFileName,"\nFileds = ",Fields, "Index = ", Index
	
	#проверка корректности Index
	if Index < 0:
		print('Index меньше 0 и равен ', Index)
		sys.exit(0)	
	if Index > BD_Info[checkdso_records]:
		print('Index больше количества записей и равен ', Index, " Колчество записей равно ", BD_Info[checkdso_records])
		sys.exit(0)	
	#Вычислить смещение
	offset = Index*BD_Info[checkdso_size_record]
	bd_file=open(DSOFileName,'rb')
	bd_file.seek(offset)
	pointer = bd_file.read(BD_Info[checkdso_size_record])

	if pointer :
####################################		integ = struct.unpack(self.UnpackFields[0],pointer)
		integ = struct.unpack(Fields[0][readini_unpackstr],pointer)
#			print pointer, integ
		wline = `integ[0]`
#			print wline

		pointer = bd_file.read( self.FieldSize[1])
		integ = unpack(self.UnpackFields[1],pointer)
#			print pointer, integ[0]
		wline +="\t"+ `integ[0]`

		print wline

		pointer = bd_file.read( self.FieldSize[2])
		integ = unpack(self.UnpackFields[2],pointer)
#			print pointer, integ
		wline +="\t"+ `integ[0]`+"\n"

		print wline
		f.write(wline)

		pointer = bd_file.read( self.FieldSize[0])
#			print "(file_size - bd_file.tell())=", (file_size - bd_file.tell())
		f.close()

	

	
def ReadDSO(DSOFileName, Fields, BD_Info):
	print "\nФайл dso_tools.py функция ReadDSO\n"
	
	print "\nDSOFN=", DSOFileName,"\nFileds=",Fields, "\nBD_Info = ",BD_Info
	
	ReadRecord(DSOFileName, Fields,BD_Info, 0)

#
"""import sys, os, stat, string
#from PyQt4 import QtGui
from PyQt4 import QtCore
from struct import *


class OpenFile(QtGui.QMainWindow):
#	FieldList
	print "class OpenFile(QtGui.QMainWindow):"
	FieldList = QtCore.QStringList()
	
	#список с размерами полей
	FieldSize = []
	#список со строками типов для функции unpack
	UnpackFields = []
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		print "\nclass OpenFile: def __init__"
		BDFileName=QtCore.QString()
		IniFileName=QtCore.QString()

		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('OpenFile')
		self.statusBar()
		self.setFocus()
		
		exit = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
		exit.setShortcut('Ctrl+O')
		exit.setStatusTip('Open new File')
		self.connect(exit, QtCore.SIGNAL('triggered()'), self.showDialog)
		menubar = self.menuBar()
		file = menubar.addMenu('&File')
		file.addAction(exit)

	def showDialog(self):
		print "\nclass OpenFile: def ShowDialog"
		##########################################################################################
		#Раскоментить в потом
		#########################################################################################
#		self.BDFileName = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home/corvin')
#		self.IniFileName = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home/corvin')
		self.BDFileName="/home/corvin/Programizm/Python/ForwardBD/reports/sut/Repdata.dso"
		self.IniFileName="/home/corvin/Programizm/Python/ForwardBD/reports/sut/RepData.ini"
		print self.BDFileName
		print self.IniFileName
		self.OpenIniFile()
		self.WriteBDFile()

#Функция разбора ини-файла
	def OpenIniFile(self):
		print "\nclass OpenFile: def OpenIniFile"
		ini=QtCore.QSettings(self.IniFileName,QtCore.QSettings.IniFormat)
		FieldCount = ini.value("Fields/Number",-1000).toInt()
		
		if FieldCount[0] <= 0:
			return
		
		print FieldCount
		self.FieldList.clear()
#    //На каждое поле (fields) по 2 строки: 1я тип, 2я имя
		for i in range(FieldCount[0]):
			ii=QtCore.QString()
			ii.setNum(i+1)
			s = QtCore.QString("Field")
			s+=ii
			s+="/Type"
			self.FieldList.append(ini.value(s).toString());
			#сохранение размера поля			
			if ini.value(s).toString() == "ftInteger":
				self.FieldSize.append(4)
				self.UnpackFields.append('=i')
				print "Field type=integer, size 4"
			
			elif ini.value(s).toString() == "ftFloat":
				self.FieldSize.append(8)
				self.UnpackFields.append('=d')
				print "Field type=double, size 8"

			else:
				print "ERROR: not found size of type ", ini.value(s).toString()

#        //FieldList.append(s);
			s="Field";
			s+=ii;
			s+="/Name";
			self.FieldList.append(ini.value(s).toString());
#        //FieldList.append(s);
		print "Содержимое FiledList: ", self.FieldList.join(QtCore.QString(", "))
		print "Содержимое FieldSize: ", self.FieldSize
		print "Содержимое UnpackFields: ", self.UnpackFields
		
		#вычисление размера одной записи
		size_record=0
		for i in range(len(self.FieldSize)):
			size_record+=self.FieldSize[i]
		print "Размер одной записи в байтах: ", size_record

		#вычисление количества записей
		file_size=os.stat(self.BDFileName)[stat.ST_SIZE]
		print "Размер файла БД в байтах:", file_size

		records = file_size/size_record
		kratno = records*size_record - file_size
		if kratno == 0 :
			print "ОК: Размер файла кратен размеру записи. Количество записей ", records
		else:
			print "ОШИБКА: размер файла не кратен размеру записи"


#Функция записи файла базы данных из тестовика
	def WriteBDFile(self):
		print "\nclass OpenFile: def ReadBDFile"

		f = open('BDinText.txt','rb')

		outf = open('CopyBD.dso','wb')
		print f

		line1 = f.readline()

		while line1 :

			line2 = line1.split()
			print "line1=", line1
			print "line2=", line2
			int1 = string.atoi(line2[0])
			int2 = string.atoi(line2[1])
			dbl = string.atof(line2[2])
			delta=0.0
			delta=28239.552734375 - dbl
	
			print int1,", ",int2,", ",dbl, ", ",delta

			data_to_write = pack("iid",int1,int2,dbl)
			print data_to_write
			outf.write(data_to_write)
			line1 = f.readline()

		f.close()
		outf.close()
		print "Write OK"

#Функция чтение файла базы данных в текстовый файл
	def ReadBDFile(self):
		print "\nclass OpenFile: def ReadBDFile"

		f = open('BDinText.txt','wb')
		print f
		bd_file=open(self.BDFileName,'rb')
#		bd_file.open(QtCore.QIODevice.ReadOnly)

#		data_stream= QtCore.QDataStream(bd_file)

		pointer = 1
		
		file_size=os.stat(self.BDFileName)[stat.ST_SIZE]
		pointer = bd_file.read( self.FieldSize[0])

		while pointer :
			
			integ = unpack(self.UnpackFields[0],pointer)
#			print pointer, integ
			wline = `integ[0]`
#			print wline

			pointer = bd_file.read( self.FieldSize[1])
			integ = unpack(self.UnpackFields[1],pointer)
#			print pointer, integ[0]
			wline +="\t"+ `integ[0]`

			print wline

			pointer = bd_file.read( self.FieldSize[2])
			integ = unpack(self.UnpackFields[2],pointer)
#			print pointer, integ
			wline +="\t"+ `integ[0]`+"\n"

			print wline
			f.write(wline)

			pointer = bd_file.read( self.FieldSize[0])
#			print "(file_size - bd_file.tell())=", (file_size - bd_file.tell())
		f.close()
		print "Readed OK"

"""

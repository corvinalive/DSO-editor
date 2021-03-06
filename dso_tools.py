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
#	print "\nФайл dso_tools.py функция ReadIni\n", "\nИмя ini-файла:", ini_file_name

	config = ConfigParser.ConfigParser()
	config.read(ini_file_name)

	if not config.has_section('Fields'):
		print(u'В ini файле не обнаружена секция "Fields"')
		sys.exit(0)

	FieldCount = config.getint("Fields","Number")
#	print "FieldCount=", FieldCount

	if FieldCount <= 0:
		print(u'В ini количество полей <= 0 (Fields)')
		sys.exit(0)

	Fields =[]
	for i in range(FieldCount):
		s = "Field"+str(i+1)
		fld_type = string.lower(config.get(s,"Type"))
#		print s," field_type=",fld_type

		fld_name = config.get(s,"Name")
#		print s," field_name=",fld_name

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
			size=string.atoi(config.get(s,"Size"))+1
			unpackstr='=s'
			
		else:
			print u"Ошибка: not found size of type ", fld_type
			sys.exit(0)

		Fields.append((fld_type,fld_name,size, unpackstr))

#	print "Fields=\n",Fields
	return Fields

def CheckDSO(DSOFileName, Fields):
#	print "\nФайл dso_tools.py функция CheckDSO\n"
	#вычисление размера одной записи
	size_record=0
	for i, item in enumerate(Fields):
		size_record += item[readini_size]
	print u"Размер одной записи ", size_record

	#вычисление количества записей
	file_size=os.stat(DSOFileName)[stat.ST_SIZE]
	print u"Размер файла БД в байтах:", file_size

	records = file_size/size_record
	kratno = records*size_record - file_size
	if kratno == 0 :
		print u"ОК: Размер файла кратен размеру записи. Количество записей ", records
	else:
		print u"ОШИБКА: размер файла не кратен размеру записи. Возможно, файл поврежден"
		sys.exit(0)

	BD_Info = (file_size, size_record, records)

#	print "BD_Info=",BD_Info
	return BD_Info



def ReadRecord(DSOFileName, Fields, BD_Info, Index):
#	print "\nФайл dso_tools.py функция ReadRecord\n"
	
#	print "\nDSOFN = ", DSOFileName,"\nFileds = ",Fields, "Index = ", Index
	
	#проверка корректности Index
    if Index < 0:
        print(u'Index меньше 0 и равен ', Index)
        sys.exit(0)	
    if Index > BD_Info[checkdso_records]:
        print(u'Index больше количества записей и равен ', Index, " Колчество записей равно ", BD_Info[checkdso_records])
        sys.exit(0)	
	#Вычислить смещение
    offset = Index*BD_Info[checkdso_size_record]
    bd_file=open(DSOFileName,'rb')
    bd_file.seek(offset)
	
	#Прочитать запись в память
    pointer = bd_file.read(BD_Info[checkdso_size_record])
    #Разбираем запись
	#wline = ""
    
    if pointer :
        
        offset_in_record = 0
        wline = []

		#перебираем все поля
        for field in Fields :
#			print field

			#Читаем текстовое поле
            if field[readini_fld_type] == "ftstring" :
				#копируем в строку
                str_from_pointer = pointer[offset_in_record : offset_in_record+(field[readini_size]-1)]
				
				#обрезаем лишнее (после нулевого байта
                str_from_pointer = str_from_pointer[0:(string.index(str_from_pointer,'\0'))]

				#декодируем строку из виндовс-кодировки
                str_from_pointer = str_from_pointer.decode('windows-1251')
                wline.append(str_from_pointer)
				#wline+="\t"

            else:
			#Читаем числа
                number = struct.unpack( field[readini_unpackstr],pointer[offset_in_record : (offset_in_record+field[readini_size])])
#				print number[0]
                wline.append(number[0])
				#wline+="\t"
            offset_in_record+=field[readini_size]
#			print offset_in_record
			
    return wline


	

	
def ReadDSO(DSOFileName, Fields, BD_Info,out_fn):
#	print "\nФайл dso_tools.py функция ReadDSO\n"
	
#	print "\nDSOFN=", DSOFileName,"\nFields=",Fields, "\nBD_Info = ",BD_Info
	f = open(out_fn,'wb');
	for i in range(BD_Info[checkdso_records]):
		s=ReadRecord(DSOFileName, Fields,BD_Info, i)
        
		s+="\n"
		f.write(s.encode('cp1251'))
	f.close()
#

#функция записи в файл одной записи (строки) из текстовика в файл БД
#
def WriteRecord(Fields, data_in_str,out_file):
	#перебираем все поля
	offset = 0
	for field in Fields :
		#разделяем строку на подстроки с разделителем табуляция
		new_offset = data_in_str[offset:].index('\t')
		field_str=data_in_str[offset : (offset+new_offset)]
#		print new_offset, " = new_offset, offset = ", offset, "str=", field_str
		offset+= new_offset+1

		#Записываем текстовое поле
		if field[readini_fld_type] == "ftstring" :
			str_fmt = str(field[readini_size])
			str_fmt+="s"
			if new_offset == 0:
				out_data = struct.pack(str_fmt,"")
			else:
				out_data = struct.pack(str_fmt,field_str)
			#пишем в файл
			out_file.write(out_data)
			
		elif field[readini_fld_type] == "ftinteger" :
		#Пишем числа integer
#			print field_str
			number = string.atoi(field_str)
			out_data = struct.pack("i",number)
			#пишем в файл
			out_file.write(out_data)
			
		elif field[readini_fld_type] == "ftfloat" :
		#Пишем числа float
#			print field_str
			number = string.atof(field_str)
			out_data = struct.pack("d",number)
			#пишем в файл
			out_file.write(out_data)

		else:
			print u"Ошибка при записи в dso: не найдем тип " , field[readini_fld_type]
			sys.exit(0)

def WriteRecord2(out_file, record, ini_data):
	#перебираем все поля записи
    offset = 0
    fieldcount=len(ini_data)
    for i in range(fieldcount):
        field = ini_data[i]
        data=record[i]
		#Записываем текстовое поле
        if field[readini_fld_type] == "ftstring" :
            #print "data=",data
            str_fmt = str(field[readini_size])
            str_fmt+="s"
            if len(data) == 0:
                emptystr=""
                out_data = struct.pack(str_fmt,emptystr.encode('windows-1251'))
            else:
                out_data = struct.pack(str_fmt,data.encode('windows-1251'))
			#пишем в файл
            out_file.write(out_data)
			
        elif field[readini_fld_type] == "ftinteger" :
		#Пишем числа integer
            out_data = struct.pack("i",data)
            #пишем в файл
            out_file.write(out_data)
			
        elif field[readini_fld_type] == "ftfloat" :
            #Пишем числа float
            out_data = struct.pack("d",data)
            #пишем в файл
            out_file.write(out_data)
        else:
            print u"Ошибка при записи в dso: не найдем тип " , field[readini_fld_type]
            sys.exit(0)


#Функция записи из текстовика в файл БД
#файл со входными данными, имя выходного файла, данные (кортеж) с данными ReadIni
def WriteDSO(in_file,out_file,Fields):
	f = open(in_file,'rb')
	
	f_out = open(out_file,'wb')
	while 1:
		l = f.readline()
		if not l:
			break
		WriteRecord(Fields,l,f_out);
	
	f.close()
	f_out.close()

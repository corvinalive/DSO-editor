#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       dso-edit.py
#       Редактор баз данных Форвард (*.dso). GUI
#       
#       Copyright 2011 Unknown <corvin@Amber>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from PySide import QtCore, QtGui, QtSql
import dso_tools
import time, string, os, shutil, sys
from dso_gui import Ui_MainWindow


class DSODB:
    def __init__(self,dso_filename):
        #Читаем ini-файл
        inifn=dso_filename
        inifn=inifn[0:(len(inifn)-4)]
        inifn+=".ini"
        print inifn
    
        #Читаем и и разбираем ini-фалй
        self.ini_data=dso_tools.ReadIni(inifn)
    
        #Проверяем размер записи, кол-во записей
        self.dso_info=dso_tools.CheckDSO(dso_filename,self.ini_data)
    
        #Буффер с данными
        self.Buffer =[]
        #Читаем файл в буфер
        for j in range(self.dso_info[dso_tools.checkdso_records]):
            rr = dso_tools.ReadRecord(dso_filename, self.ini_data, self.dso_info, j)
            self.Buffer.append(rr)
            
    def GetColCount(self):
        return len(self.Buffer[0])
            
    def GetRowCount(self):
        return len(self.Buffer)

class MyMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
    def FillTable(self,dsodata):
        columnCount = dsodata.GetColCount()
        rowCount = dsodata.GetRowCount()
    
        tableWidget =self.ui.tableWidget
        tableWidget.setRowCount(rowCount)
        tableWidget.setColumnCount(columnCount)
        #Заполним названия колонок
        labels=[]
        for i in dsodata.ini_data:
            labels.append(i[dso_tools.readini_fld_name])
        tableWidget.setHorizontalHeaderLabels(labels)
        #заполним содержимое ячеек
        for j in range(rowCount):
            record=dsodata.Buffer[j]
            for i in range(len(record)):
                s=" ";
                if dsodata.ini_data[i][dso_tools.readini_fld_type] == "ftstring" :
                    s=record[i]
                else:
                    s=str(record[i])
                newItem = QtGui.QTableWidgetItem(s)
                tableWidget.setItem(j,i, newItem)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = MyMainWindow()
    
    #Выбираем файл БД
    #fileName = QtGui.QFileDialog.getOpenFileName(None,
    #u"Открыть файл БД", "", "Forward Data base Files (*.dso)")
    fileName="/home/corvin/Programizm/Python/FWPython/DSO-editor/xset.dso","."

    #Делаем бэкап открываемого файла, если он есть
    #t=time.localtime(time.time())
    #backfn=fileName[0]+" "+str(t[0])+" "+string.zfill(str(t[1]),2)+" "+string.zfill(str(t[2]),2)+" "+string.zfill(str(t[3]),2)+string.zfill(str(t[4]),2)+string.zfill(str(t[5]),2)
    
    if os.path.exists(fileName[0]):
        #shutil.copyfile(fileName[0],backfn)
        print u"Была создана резервная копия файла ",fileName, u"под именем "#, backfn
    else:
        sys.exit(app.exec_())

    fileName=fileName[0]
    dsodata = DSODB(fileName)
    myapp.FillTable(dsodata)

    myapp.show()
    sys.exit(app.exec_())

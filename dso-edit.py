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


#import PySide.QtCore #import *
#import PySide.QtGui #import *
#import sys
 
 
# Create a Qt application 
#app = QApplication(sys.argv)
# Create a Label and show it
#label = QTableView ()
#label.show()
# Enter Qt application main loop
#app.exec_()
#sys.exit()

	

from PySide import QtCore, QtGui, QtSql
import dso_tools
import time, string, os, shutil



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    
    #Выбираем файл БД
    #fileName = QtGui.QFileDialog.getOpenFileName(None,
    #u"Открыть файл БД", "", "Forward Data base Files (*.dso)")
    fileName="/home/corvin/Programizm/Python/FWPython/DSO-editor/xset.dso","."

    #Делаем бэкап открываемого файла, если он есть
    t=time.localtime(time.time())
    backfn=fileName[0]+" "+str(t[0])+" "+string.zfill(str(t[1]),2)+" "+string.zfill(str(t[2]),2)+" "+string.zfill(str(t[3]),2)+string.zfill(str(t[4]),2)+string.zfill(str(t[5]),2)
    
    if os.path.exists(fileName[0]):
        shutil.copyfile(fileName[0],backfn)
        print u"Была создана резервная копия файла ",fileName, u"под именем ", backfn
    else:
        sys.exit(app.exec_())

    fileName=fileName[0]
    #Читаем ini-файл
    inifn=fileName
    inifn=inifn[0:(len(inifn)-4)]
    inifn+=".ini"
    print inifn
    
    #Читаем и и разбираем ini-фалй
    x=dso_tools.ReadIni(inifn)
    
    #Проверяем размер записи, кол-во записей
    y=dso_tools.CheckDSO(fileName,x)
    
    columnCount = len(x)
    rowCount = y[dso_tools.checkdso_records]
    

    
    tableWidget =QtGui.QTableWidget()
    tableWidget.setRowCount(rowCount)
    tableWidget.setColumnCount(columnCount)

    rr = dso_tools.ReadRecord(fileName, x, y, 0)

#    newItem = QtGui.QTableWidgetItem(rr[0])
#    tableWidget.setItem(0,0, newItem)

    newItem1 = QtGui.QTableWidgetItem("14")
    tableWidget.setItem(0,1, newItem1)
    #print rr, len(rr)
#    for i in range(len(rr)):
    for i in range(25):
        print "i=", i," class=", rr[i].__class__
        s=" ";
        s=rr[i]
        if rr[i].__class__ == "<type 'int'>":
            print "int found"
            s="int"
        
        newItem = QtGui.QTableWidgetItem(rr[i])
        tableWidget.setItem(0,i, newItem)
    #    if rr[i] == "" :
     #       print "rr[i]=None"
      #  else:
       #     sss=""
        #    if rr[i].__class__ == "int":
         #       sss="11"
            
          #  elif rr[i].__class__ == "unicode":
           #     sss = str(rr[i].encode('Utf8'))
            #print "sss=",sss
            #newItem = QtGui.QTableWidgetItem(sss)
            #tableWidget.setItem(0,i, newItem)

    tableWidget.show()
    sys.exit(app.exec_())

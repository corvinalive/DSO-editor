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

class Node:
    def __init__(self, value = None, next = None):
        self.value = value
        self.next = next
        
class LinkedList:
    def __init__(self):
        self.first = None
        self.last = None
        self.length = 0

    def __str__(self):
        if self.first != None:
            current = self.first
            out = 'LinkedList [\n' +str(current.value) +'\n'
            while current.next != None:
                current = current.next
                out += str(current.value) + '\n'
            return out + ']'
        return 'LinkedList []'

    def clear(self):
        self.__init__()
    #добавление в конец списка
    def add(self, x):
        if self.first == None:
            self.first = Node(x, None)
            self.last = self.first
        elif self.last == self.first:
            self.last = Node(x, None)
            self.first.next = self.last
        else:
            current = Node(x, None)
            self.last.next = current
            self.last = current                
        
    def Len(self):
        self.length =0
        if self.first != None:
            self.length +=1
            current = self.first
            while current.next != None:
                current = current.next
                self.length +=1
        return self.length
   
   #добавить в указаннную позицию
    def InsertNth(self,i,x):
        if (self.first == None):
            self.first = Node(x,self.first)
            self.last = self.first.next
            return
        if i == 0:
          self.first = Node(x,self.first)
          return
        curr=self.first
        count = 0
        while curr != None:
            if count == i-1:
              curr.next = Node(x,curr.next)
              if curr.next.next == None:
                self.last = curr.next
              break
            curr = curr.next
   
    def Del(self,i):
        if (self.first == None):
          return
        old = curr = self.first
        count = 0
        if i == 0:
          self.first = self.first.next
          return
        while curr != None:
            print "count=",count," index=",i
            if count == i:
              if curr.next == self.last:
                self.last = curr
                break
              else:
                old.next = curr.next 
              break
            old = curr  
            curr = curr.next
            count += 1
        
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
        self.Buffer = LinkedList()
        #Читаем файл в буфер
        for j in range(self.dso_info[dso_tools.checkdso_records]):
            rr = dso_tools.ReadRecord(dso_filename, self.ini_data, self.dso_info, j)
            self.Buffer.add(rr)
            
    def GetColCount(self):
        return len(self.ini_data)
            
    def GetRowCount(self):
        return self.Buffer.Len()
    
    def delRow(self,index):
        self.Buffer.Del(index)
    
    def addRow(self,index):
        newrecord = []
        for i in range(len(self.ini_data)):
            s=" ";
            if self.ini_data[i][dso_tools.readini_fld_type] == "ftstring" :
                newrecord.append(u"")
            elif self.ini_data[i][dso_tools.readini_fld_type] == "ftfloat":
                newrecord.append(0.0)
            elif self.ini_data[i][dso_tools.readini_fld_type] == "ftinteger":
                newrecord.append(0)
            else:
                print "ERROR! at DSODB.addRow() неизвестный тип"
        print newrecord
        self.Buffer.InsertNth(index,newrecord)


class MyMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect(self.ui.delRowButton, QtCore.SIGNAL("clicked()"), self.pushButtondelete)
        self.connect(self.ui.AddRowBeforeButton, QtCore.SIGNAL("clicked()"), self.pushButtonaddbefore)
        self.connect(self.ui.AddButtonAfterButton, QtCore.SIGNAL("clicked()"), self.pushButtonaddafter)
        self.connect(self.ui.SavenExitButton, QtCore.SIGNAL("clicked()"), self.pushButtonsavenexit)
        self.connect(self.ui.ClosewoSaveButton, QtCore.SIGNAL("clicked()"), self.pushButtonexitwosave)


    def pushButtondelete(self):
        i = self.ui.tableWidget.currentRow()
        msgBox = QtGui.QMessageBox()
        msgBox.setText(u"Удаление строки")
        msg=u"Удалить строку номер "
        msg+=str(i)
        print msg
        msgBox.setInformativeText(msg)
        msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No )
        msgBox.setDefaultButton(QtGui.QMessageBox.No)
        ret=msgBox.exec_()
        if ret == QtGui.QMessageBox.Yes:
            print "button delete pressed. now call self.dsodata.delRow(i)"
            self.dsodata.delRow(i)
            print "self.dsodata.delRow(i) is ok. now call Filltable()"
            self.FillTable()
            #self.ui.tableWidget.removeRow(i)
            print "Filltable() ok"
        

    def pushButtonaddbefore(self):
        self.dsodata.addRow(self.ui.tableWidget.currentRow())
        self.FillTable()

    def pushButtonaddafter(self):
        self.dsodata.addRow(self.ui.tableWidget.currentRow()+1)
        self.FillTable()

    def pushButtonsavenexit(self):
        s=":SA"'\15'

    def pushButtonexitwosave(self):
        s=":SA"'\15'
    
    def SetData(self,dsodata):
        self.dsodata=dsodata
        self.FillTable()
        
    def FillTable(self):
        columnCount = self.dsodata.GetColCount()
        print "Columncount=", columnCount
        rowCount = self.dsodata.GetRowCount()
        print "rowcount=",rowCount
    
        tableWidget =self.ui.tableWidget
        tableWidget.setRowCount(rowCount)
        tableWidget.setColumnCount(columnCount)
        tableWidget.clear()
        print "Set row n col count completed"
        #Заполним названия колонок
        labels=[]
        for i in self.dsodata.ini_data:
            labels.append(i[dso_tools.readini_fld_name])
        tableWidget.setHorizontalHeaderLabels(labels)
        print "заполнили заголовки"
        #заполним содержимое ячеек
        record=self.dsodata.Buffer.first
        for j in range(rowCount):
            print "заполняем строку ",j
            recvalue=record.value
            for i in range(len(recvalue)):
                s=" ";
                if self.dsodata.ini_data[i][dso_tools.readini_fld_type] == "ftstring" :
                    s=recvalue[i]
                else:
                    s=str(recvalue[i])
                newItem = QtGui.QTableWidgetItem(s)
                tableWidget.setItem(j,i, newItem)
            record=record.next

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = MyMainWindow()
    
    #Выбираем файл БД
    fileName = QtGui.QFileDialog.getOpenFileName(None,
    u"Открыть файл БД", "", "Forward Data base Files (*.dso)")
    #fileName="/home/corvin/Programizm/Python/FWPython/DSO-editor/xset.dso","."

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
    myapp.SetData(dsodata)

    myapp.show()
    sys.exit(app.exec_())

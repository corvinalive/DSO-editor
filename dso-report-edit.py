#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       dso-report-edit.py
#       Редактор отчетов баз данных Форвард (*.dso). GUI
#       
#       Copyright 2011 Unknown <corvinalive@yandex.ru>
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
import dso_tools, linked_list
import time, string, os, shutil, sys
from dso_report_gui import Ui_MainWindow

        
        
class DSODB:
    def __init__(self,dso_filename):
        self.dso_filename=dso_filename
        #Читаем ini-файл
        inifn=dso_filename
        inifn=inifn[0:(len(inifn)-4)]
        inifn+=".ini"
        #print inifn
    
        #Читаем и и разбираем ini-фалй
        self.ini_data=dso_tools.ReadIni(inifn)
        
    
        #Проверяем размер записи, кол-во записей
        self.dso_info=dso_tools.CheckDSO(dso_filename,self.ini_data)
    
        #Буффер с данными
        self.Buffer = linked_list.LinkedList()
        
        #Буфер с отчетами
        self.Reports = linked_list.LinkedList()
        #Читаем файл в буфер
        for j in range(self.dso_info[dso_tools.checkdso_records]):
            rr = dso_tools.ReadRecord(dso_filename, self.ini_data, self.dso_info, j)
            self.Buffer.add(rr)
        self.CheckIsReport()
            
        
    def CheckIsReport(self):
        #Проверка кол-ва полей. У отчетов их должно быть 3:
        if len(self.ini_data) !=3 :
            print "ОШИБКА! Количество полей равно ", len(self.ini_data), "у отчетов оно равно 3.\nАварийный выход"
            sys.exit(1)
        
        #Определим назначение полей
        self.cellvalue=0 #значение ячейки
        self.report_num=0 #номер отчета
        self.uninum = 0 #номер точки
        
        #Найдем, в каком поле хранится значение ячейки
        for i in range(len(self.ini_data)):
            field=self.ini_data[i]
            if field[dso_tools.readini_fld_type] == "ftfloat" :
                print "Значение ячейки хранится в поле №", i
                self.cellvalue=i
                break
                
        #Найдем, где находится номер отчета и номер точки
        rec1 = self.Buffer.first
        rec2 = rec1.next
        
        for i in range(len(self.ini_data)):
            field=self.ini_data[i]
            if field[dso_tools.readini_fld_type] == "ftinteger" :
                if rec1.value[i] == rec2.value[i] : #Нашли, где находится номер отчета
                    self.report_num=i
                    print "Номер отчета хранится в поле №", self.report_num
                else:
                    self.uninum=i
                    print "Номер точки хранится в поле №", self.uninum

        #Определяем кол-во строк в одном отчете, состав отчета, сравниваем одинаковость во всей базе
        buf_len = self.Buffer.Len()
        self.rows_in_report = 0 #кол-во строк в одном отчете
        self.report_data = [] #состав отчета
        
        self.report_data.append(u"№ отчета")
        
        cur_rec = self.Buffer.first
        self.report_data.append(cur_rec.value[self.uninum])
        for i in range(buf_len):
            next_rec=cur_rec.next
            if cur_rec.value[self.report_num] == next_rec.value[self.report_num] :
                self.report_data.append(next_rec.value[self.uninum])
                cur_rec = next_rec
            else:
                break
        self.row_in_report= len(self.report_data)-1
        
        print "Кол-во строк в отчете равно ", self.row_in_report
        print "Отчет содержит след. данные: ",self.report_data
        
        #Определяем кол-во отчетов в базе данных:
        self.count_reports_in_dso = buf_len / self.row_in_report
        print "Кол-во отчетов: ",self.count_reports_in_dso
        
        #Заполнение буфера с отчетами
        cur_rec = self.Buffer.first
        counter = 0
        while 1:
            cur_rep=[]
            #номер текущего отчета
            cur_rep_num = cur_rec.value[self.report_num]
            cur_rep.append(str(cur_rep_num))
            
            for i in range(len(self.report_data)-1):
                #проверка одинаковости номер отчета
                if cur_rec.value[self.report_num] != cur_rep_num:
                    print "ОШИБКА! Некорректный номер отчета в записи №", counter
                    sys.exit(1)
                if cur_rec == None:
                    print "ОШИБКА! Преждевременно закончились записи в БД"
                    sys.exit(1)
                #проверка равенства uninum в формате отчета и записи
                if cur_rec.value[self.uninum] == self.report_data[i+1]:
                    cur_rep.append(cur_rec.value[self.cellvalue])
                else:
                    print "ОШИБКА! Не совпадает запись № ", counter, " в БД с форматом отчета"
                    sys.exit(1)
                cur_rec = cur_rec.next
                counter+=1
            self.Reports.add(cur_rep)
            if cur_rec == None:
                break

    def GetRepColCount(self):
        return len(self.report_data)
            
    def GetRepRowCount(self):
        return self.Reports.Len()
    
    def delRow(self,index):
        #Удаляем данные из списка записей
        len_rep = len(self.report_data-1)
        rec_index = index*len_rep
        for i in range(len_rep):
            self.Buffer.Del(rec_index)
        #удаляем данные из списка отчетов
        self.Reports.Del(index)
    
    def addRow(self,index):
        #print "addrow index=",index
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
        #print newrecord
        self.Buffer.InsertNth(index,newrecord)
        #print "addrow return"
        
    def Save(self):
        #Делаем бэкап открываемого файла, если он есть
        fn = os.path.split(self.dso_filename)
        t=time.localtime(time.time())
        fnn=str(t[0])+" "+string.zfill(str(t[1]),2)+" "+string.zfill(str(t[2]),2)\
                +" "+string.zfill(str(t[3]),2)+string.zfill(str(t[4]),2)\
                +string.zfill(str(t[5]),2)+" "+fn[1]
        backfn = os.path.join(fn[0],fnn)
        #print "backfn=",backfn
        if os.path.exists(self.dso_filename):
            shutil.copyfile(self.dso_filename,backfn)
            print u"Была создана резервная копия файла ",self.dso_filename, u"под именем ", backfn
        else:
            sys.exit(app.exec_())

        f_out = open(self.dso_filename,'wb')
        #Перебираем записи и пишем их
        current=self.Buffer.first
        while 1:
            if current == None:
                return
            #print current.value
            dso_tools.WriteRecord2(f_out, current.value, self.ini_data)
            current=current.next
        f_out.close()

class MyMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.now_is_insert_row = False
        self.connect(self.ui.delRowButton, QtCore.SIGNAL("clicked()"), self.pushButtondelete)
        self.connect(self.ui.AddRowBeforeButton, QtCore.SIGNAL("clicked()"), self.pushButtonaddbefore)
        self.connect(self.ui.AddButtonAfterButton, QtCore.SIGNAL("clicked()"), self.pushButtonaddafter)
        self.connect(self.ui.SavenExitButton, QtCore.SIGNAL("clicked()"), self.pushButtonsavenexit)
        self.connect(self.ui.ClosewoSaveButton, QtCore.SIGNAL("clicked()"), self.pushButtonexitwosave)
        self.ui.tableWidget.connect(self.ui.tableWidget, QtCore.SIGNAL("cellChanged(int, int)"),self.CellDataSave)

    def CellDataSave(self,row,column):
        if self.now_is_insert_row == False:
            #print "Data changed in row=",row," column=",column
            item = self.ui.tableWidget.item(row,column)
            #print item.text()
            #Найдем строку в данных
            record = self.dsodata.Buffer.ItemAt(row)
            #print "Record.value=",record.value
            if self.dsodata.ini_data[column][dso_tools.readini_fld_type] == "ftstring" :
                record.value[column]=item.text()
            elif self.dsodata.ini_data[column][dso_tools.readini_fld_type] == "ftfloat":
                val = 0.0
                try:
                    val = string.atof(item.text())
                except ValueError, TypeError:
                    pass
                record.value[column]=val
                item.setText(str(val))
            elif self.dsodata.ini_data[column][dso_tools.readini_fld_type] == "ftinteger":
                val = 0
                try:
                    val = string.atoi(item.text())
                except ValueError, TypeError:
                    pass
                record.value[column]=val
                item.setText(str(val))
        
    def pushButtondelete(self):
        i = self.ui.tableWidget.currentRow()
        msgBox = QtGui.QMessageBox()
        msgBox.setText(u"Удаление строки")
        msg=u"Удалить строку номер "
        msg+=str(i)
        msgBox.setInformativeText(msg)
        msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No )
        msgBox.setDefaultButton(QtGui.QMessageBox.No)
        ret=msgBox.exec_()
        if ret == QtGui.QMessageBox.Yes:
            self.dsodata.delRow(i)
            self.ui.tableWidget.removeRow(i)
        
    def Add(self,index):
        irow=index
        self.dsodata.addRow(irow)
        self.now_is_insert_row=True
        self.ui.tableWidget.insertRow(irow)
        #заполним информацию
        recvalue=self.dsodata.Buffer.ItemAt(irow).value
        for i in range(len(recvalue)):
            s=" ";
            if self.dsodata.ini_data[i][dso_tools.readini_fld_type] == "ftstring" :
                s=recvalue[i]
            else:
                s=str(recvalue[i])
            newItem = QtGui.QTableWidgetItem(s)
            self.ui.tableWidget.setItem(irow,i,newItem)
        self.now_is_insert_row = False

    def pushButtonaddbefore(self):
        irow=self.ui.tableWidget.currentRow()
        self.Add(irow)
        

    def pushButtonaddafter(self):
        irow=self.ui.tableWidget.currentRow()+1
        self.Add(irow)

    def pushButtonsavenexit(self):
        self.dsodata.Save()
        self.close()

    def pushButtonexitwosave(self):
        self.close()
    
    def SetData(self,dsodata):
        self.dsodata=dsodata
        self.FillTable()
        
    def FillTable(self):
        self.now_is_insert_row = True
        columnCount = self.dsodata.GetRepColCount()
        rowCount = self.dsodata.GetRepRowCount()
    
        tableWidget =self.ui.tableWidget
        tableWidget.setRowCount(rowCount)
        tableWidget.setColumnCount(columnCount)
        tableWidget.clear()
        #Заполним названия колонок
        labels=[]
        labels.append(self.dsodata.report_data[0])
        for i in range(len(self.dsodata.report_data)-1):
            labels.append(str(self.dsodata.report_data[i+1]))
        tableWidget.setHorizontalHeaderLabels(labels)
        #заполним содержимое ячеек
        record=self.dsodata.Reports.first
        for j in range(rowCount):
            recvalue=record.value
            for i in range(len(recvalue)):
                s=str(recvalue[i])
                newItem = QtGui.QTableWidgetItem(s)
                tableWidget.setItem(j,i, newItem)
            record=record.next
        self.now_is_insert_row = False

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = MyMainWindow()
    
    #Выбираем файл БД
    #fileName = QtGui.QFileDialog.getOpenFileName(None,
    #u"Открыть файл БД", "", "Forward Data base Files (*.dso)")
    fileName="/home/corvin/Programizm/Python/DSO-editor/repdata.dso","."
    
    if os.path.exists(fileName[0]):
        pass
    else:
        sys.exit(app.exec_())

    fileName=fileName[0]
    dsodata = DSODB(fileName)
    myapp.SetData(dsodata)

    myapp.showMaximized()
    sys.exit(app.exec_())

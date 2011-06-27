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
import connection

def initializeModel(model):
    model.setTable("person")
    model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
    model.select()
    model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
    model.setHeaderData(1, QtCore.Qt.Horizontal, "First name")
    model.setHeaderData(2, QtCore.Qt.Horizontal, "Last name")


def createView(title, model):
    view = QtGui.QTableView()
    view.setModel(model)
    view.setWindowTitle(title)
    return view


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    if not connection.createConnection():
        sys.exit(1)
    model = QtSql.QSqlTableModel()
    initializeModel(model)
    view1 = createView("Table Model (View 1)", model)
    view2 = createView("Table Model (View 2)", model)
    view1.show()
    view2.move(view1.x() + view1.width() + 20, view1.y())
    view2.show()
    sys.exit(app.exec_())

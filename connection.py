from PySide import QtSql, QtGui


def createConnection():
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(":memory:")
    if not db.open():
        QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
                QtGui.qApp.tr("Unable to establish a database connection.\n"
                              "This example needs SQLite support. Please read "
                              "the Qt SQL driver documentation for information "
                              "how to build it.\n\nClick Cancel to exit."),
                QtGui.QMessageBox.Cancel, QtGui.QMessageBox.NoButton)
        return False

    query = QtSql.QSqlQuery()
    query.exec_("create table person(id int primary key, "
                "firstname varchar(20), lastname varchar(20))")
    query.exec_("insert into person values(101, 'Danny', 'Young')")
    query.exec_("insert into person values(102, 'Christine', 'Holand')")
    query.exec_("insert into person values(103, 'Lars', 'Gordon')")
    query.exec_("insert into person values(104, 'Roberto', 'Robitaille')")
    query.exec_("insert into person values(105, 'Maria', 'Papadopoulos')")
    return True

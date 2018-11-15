from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QLineEdit, QGridLayout, QMessageBox, QDateTimeEdit
from MySQLConnector import *
from datetime import date, datetime


class FormDialog(QDialog):
    def __init__(self, db="", table="", cols=[], manager=None, parent=None):
        super(FormDialog, self).__init__(parent)
        self.manager = manager
        self.db = db
        self.table = table
        self.cols = cols

        layout = QGridLayout(self)

        self.text_boxes = []
        i = 0
        for c in cols:
            print(c)
            label = QLabel(c)
            if "int" in c:
                box = QLineEdit()
                box.box_type = "int"
                box.setValidator(QIntValidator())
            elif "date" in c:
                box = QDateTimeEdit(self)
                box.box_type = "date"
                box.setCalendarPopup(True)
                box.setDateTime(QDateTime.currentDateTime())
            else:
                box = QLineEdit()
                box.box_type = "char"

            
            self.text_boxes.append(box)
            layout.addWidget(label, i, 0)
            layout.addWidget(box, i, 1)
            i += 1


        # layout.addWidget(form)
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept(self):
        values = []
        for tb in self.text_boxes:
            if tb.box_type == "date":
                values.append(datetime( tb.dateTime().date().year(),
                                        tb.dateTime().date().month(), 
                                        tb.dateTime().date().day(),
                                        tb.dateTime().time().hour(),
                                        tb.dateTime().time().minute(),
                                        tb.dateTime().time().second(),
                                        tb.dateTime().time().msec()))
            else:
                values.append(tb.text())

        err = self.manager.insert(db=self.db,
                                  table=self.table,
                                  cols=self.cols,
                                  values=values)
        if err != None:
            msg = QMessageBox()
            msg.setText("ERROR: " + err.__doc__)
            msg.exec_()
        else:
            super(FormDialog, self).accept()

    
    @staticmethod
    def getDateTime(db="", table="", cols=[], manager=None, parent=None):
        dialog = FormDialog(parent=parent,
                            db=db,
                            table=table,
                            cols=cols,
                            manager=manager)
        dialog.exec_()
        return 1

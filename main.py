import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QGridLayout, QLineEdit, QTreeWidgetItem, \
    QTreeWidget, QTableWidget, QComboBox, QMessageBox, QTableWidgetItem, QProgressBar
from PyQt5.QtGui import QFont

from MySQLConnector import *
from PSQLConnector import PSQLConnector


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.mysqlc = MySQLConnector()
        self.psqlc = PSQLConnector()
        self.init_ui()

    def init_ui(self):
        """This initiates the window"""
        # GRID Layout
        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        # First Row
        self.server_label = QLabel("Server")
        self.server_label.setMaximumHeight(10)

        self.port_label = QLabel("Port")
        self.port_label.setMaximumHeight(10)

        self.user_label = QLabel("User")
        self.user_label.setMaximumHeight(10)

        self.password_label = QLabel("Password")
        self.password_label.setMaximumHeight(10)

        self.connect_button = QPushButton("Connect", self)
        self.connect_button.clicked.connect(self.handle_connect)

        self.grid.addWidget(self.server_label, 0, 1, 1, 1)
        self.grid.addWidget(self.port_label, 0, 2, 1, 1)
        self.grid.addWidget(self.user_label, 0, 3, 1, 1)
        self.grid.addWidget(self.password_label, 0, 4, 1, 1)
        self.grid.addWidget(self.connect_button, 1, 6, 1, 2)

        # Second row
        self.connection_box = QComboBox()
        self.connection_box.addItem("MySQL")
        self.connection_box.addItem("PostgreSQL")
        self.connection_box.currentTextChanged.connect(self.handle_connector__changed)
        self.server_input = QLineEdit()
        self.server_input.setText("127.0.0.1")
        self.port_input = QLineEdit()
        self.port_input.setText("3306")
        self.port_input.setMaximumWidth(60)
        self.user_input = QLineEdit()
        self.user_input.setText("")
        self.password_input = QLineEdit()
        self.password_input.setText("")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.grid.addWidget(self.server_input, 1, 1)
        self.grid.addWidget(self.port_input, 1, 2)
        self.grid.addWidget(self.user_input, 1, 3)
        self.grid.addWidget(self.password_input, 1, 4)
        self.grid.addWidget(self.connection_box, 1, 5, 1, 1)

        # Third row
        self.schema_tree = QTreeWidget()
        self.schema_tree.setColumnCount(1)
        self.schema_tree.setHeaderLabels(["Data bases"])
        self.schema_tree.itemDoubleClicked.connect(self.handle_tree_clicked)

        self.query_result = QTableWidget()

        self.query_input = QLineEdit()
        self.query_button = QPushButton("Run query")
        self.query_button.clicked.connect(self.handle_run_query)
        self.info_label = QLabel("")
        self.info_label.setMaximumHeight(12)
        self.info_label.setFont(QFont("SansSerif", 8))

        self.grid.addWidget(self.info_label, 2, 2, 1, 3)
        self.grid.addWidget(self.query_input, 3, 2, 1, 4)
        self.grid.addWidget(self.query_button, 3, 6, 1, 2)
        self.grid.addWidget(self.query_result, 4, 2, 4, 6)
        self.grid.addWidget(self.schema_tree, 2, 1, 6, 1)

        self.setLayout(self.grid)
        self.setWindowTitle('DB Admin')
        self.show()

    def init_schema(self):
        self.schema_tree.clear()
        for key in self.schema.keys():
            db_tree = QTreeWidgetItem([key])
            db_tree.identifier = "DATABASE"
            db_tree.text_value = key
            for table in self.schema[key].keys():
                table_tree = QTreeWidgetItem([table])
                table_tree.identifier = "TABLE"
                table_tree.text_value = table
                for column in self.schema[key][table]:
                    col = QTreeWidgetItem([column])
                    col.identifier = "COLUMN"
                    col.text_value = column
                    table_tree.addChild(col)
                db_tree.addChild(table_tree)
            self.schema_tree.addTopLevelItem(db_tree)

    def draw_table(self, result):
        self.query_result.clear()
        self.query_result.setRowCount(len(result)-1)
        self.query_result.setColumnCount(len(result[0]))
        self.query_result.setHorizontalHeaderLabels(result[0])

        for row_i in range(1, len(result)):
            for col_i in range(0, len(result[0])):
                self.query_result.setItem(row_i-1, col_i, QTableWidgetItem(str(result[row_i][col_i])))

    """         EVENT HANDLERS         """
    def show_modal(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec_()

    def handle_connector__changed(self, t):
        if t == "PostgreSQL":
            self.port_input.setText("5432")
        else:
            self.port_input.setText("3306")

    def handle_connect(self):
        if self.connection_box.currentText() == "MySQL":
            self.mysqlc.set_config(user=self.user_input.text(),
                                   host=self.server_input.text(),
                                   password=self.password_input.text(),
                                   port=self.port_input.text())
            self.schema = self.mysqlc.get_schema()
            self.init_schema()
            self.show_modal("Connection success")
        else:
            self.psqlc.set_config(user=self.user_input.text(),
                                  host=self.server_input.text(),
                                  password=self.password_input.text())
            self.schema = self.psqlc.get_schema()
            self.init_schema()
            self.show_modal("Connection success")

    def handle_run_query(self):
        if not hasattr(self, 'schema'):
            self.show_modal("You are not connected to a server")
            return

        if self.connection_box.currentText() == "MySQL":
            self.draw_table(self.mysqlc.query(self.db_use, self.query_input.text()))
        else:
            self.draw_table(self.psqlc.query(self.db_use, self.query_input.text()))

    def handle_tree_clicked(self, item):
        if self.connection_box.currentText() == "MySQL":
            if item.identifier == "DATABASE":
                self.info_label.setText(f"USE : {item.text_value}")
                self.db_use = item.text_value
            elif item.identifier == "TABLE":
                query = f"SELECT * FROM {item.text_value}"
                self.draw_table(self.mysqlc.query(self.db_use, query))
        else:
            if item.identifier == "DATABASE":
                self.info_label.setText(f"USE : {item.text_value}")
                self.db_use = item.text_value
            elif item.identifier == "TABLE":
                query = f"SELECT * FROM {item.text_value}"
                self.draw_table(self.psqlc.query(self.db_use, query))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

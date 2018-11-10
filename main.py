import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QGridLayout, QLineEdit, QTreeWidgetItem, \
    QTreeWidget, QTableWidget, QComboBox


# https://stackoverflow.com/questions/41204234/python-pyqt5-qtreewidget-sub-item

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        """This initiates the window"""
        # GRID Layout
        grid = QGridLayout()
        grid.setSpacing(5)

        # First Row
        self.server_label = QLabel("Server")
        self.server_label.setMaximumHeight(10)
        self.user_label = QLabel("User")
        self.user_label.setMaximumHeight(10)
        self.password_label = QLabel("Password")
        self.password_label.setMaximumHeight(10)
        self.connect_button = QPushButton("Connect")

        grid.addWidget(self.server_label, 0, 1, 1, 1)
        grid.addWidget(self.user_label, 0, 2, 1, 1)
        grid.addWidget(self.password_label, 0, 3, 1, 1)
        grid.addWidget(self.connect_button, 1, 5, 1, 2)

        # Second row
        self.connection_box = QComboBox()
        self.connection_box.addItem("MySQL")
        self.connection_box.addItem("PostgreSQL")
        self.server_input = QLineEdit()
        self.user_input = QLineEdit()
        self.password_input = QLineEdit()
        grid.addWidget(self.server_input, 1, 1)
        grid.addWidget(self.user_input, 1, 2)
        grid.addWidget(self.password_input, 1, 3)
        grid.addWidget(self.connection_box, 1, 4, 1, 1)

        # Third row
        self.db_tree = QTreeWidget()
        self.db_tree.setColumnCount(1)
        self.db_tree.setHeaderLabels(["Data bases"])

        self.query_result = QTableWidget()

        self.query_input = QLineEdit()
        self.query_button = QPushButton("Run query")

        grid.addWidget(self.query_input, 2, 2, 1, 3)
        grid.addWidget(self.query_button, 2, 5, 1, 2)
        grid.addWidget(self.query_result, 3, 2, 4, 5)
        grid.addWidget(self.db_tree, 2, 1, 5, 1)

        self.setLayout(grid)
        self.setWindowTitle('DB Admin')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from .model import ContactsModel


class Window(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Contacts")
        self.resize(625, 400)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.contacts_model = ContactsModel()
        self.setup_ui()

    def setup_ui(self):
        self.table = QTableView()
        self.table.setModel(self.contacts_model.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.open_add_dialog)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_contact)
        self.clear_all_button = QPushButton("Clear All")
        self.clear_all_button.clicked.connect(self.clear_contacts)
        layout = QVBoxLayout()
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addStretch()
        layout.addWidget(self.clear_all_button)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def open_add_dialog(self):
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.contacts_model.add_contact(dialog.data)
            self.table.resizeColumnsToContents()

    def delete_contact(self):
        row = self.table.currentIndex().row()
        if row < 0:
            return

        message_box = QMessageBox.warning(self,
                                         "Warning!",
                                         "Are you sure you want to remove the selected contact?",
                                         QMessageBox.Ok | QMessageBox.Cancel,
                                         )

        if message_box == QMessageBox.Ok:
            self.contacts_model.delete_contact(row)

    def clear_contacts(self):
        message_box = QMessageBox.warning(
            self,
            "Warning!",
            "Are you sure you want to remove all your contacts?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if message_box == QMessageBox.Ok:
            self.contacts_model.clear_contacts()


class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Add Contact")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setup_ui()

    def setup_ui(self):
        self.name_field = QLineEdit()
        self.name_field.setObjectName("Name")
        self.phone_field = QLineEdit()
        self.phone_field.setObjectName("Phone")
        self.job_field = QLineEdit()
        self.job_field.setObjectName("Job")
        self.email_field = QLineEdit()
        self.email_field.setObjectName("Email")
        layout = QFormLayout()
        layout.addRow("Name:", self.name_field)
        layout.addRow("Phone:", self.phone_field)
        layout.addRow("Job:", self.job_field)
        layout.addRow("Email:", self.email_field)
        self.layout.addLayout(layout)
        self.buttons_box = QDialogButtonBox(self)
        self.buttons_box.setOrientation(Qt.Horizontal)
        self.buttons_box.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttons_box.accepted.connect(self.accept)
        self.buttons_box.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons_box)

    def accept(self):
        self.data = []
        for field in (self.name_field, self.phone_field, self.job_field, self.email_field):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}",
                )
                self.data = None  # Reset .data
                return
            self.data.append(field.text())

        if not self.data:
            return

        super().accept()

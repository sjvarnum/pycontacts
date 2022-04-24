from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel


class ContactsModel:
    def __init__(self):
        self.model = self._create_model()

    @staticmethod
    def _create_model():
        table_model = QSqlTableModel()
        table_model.setTable("contacts")
        table_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        table_model.select()
        headers = ("ID", "Name", "Phone", "Job", "Email")
        for index, header in enumerate(headers):
            table_model.setHeaderData(index, Qt.Horizontal, header)

        return table_model

    def add_contact(self, data):
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()

    def delete_contact(self, row):
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def clear_contacts(self):
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

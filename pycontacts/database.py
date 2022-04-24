from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


def _create_contacts_table():
    create_table_query = QSqlQuery()
    return create_table_query.exec(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(50) NOT NULL,
            phone VARCHAR(50),
            job VARCHAR(50),
            email VARCHAR(50)
        )
        """
    )


def create_connection(database_name):
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(database_name)
    if not connection.open():
        QMessageBox.warning(None, "Contact",
                            f"Database Error: {connection.lastError().text()}")
        return False
    _create_contacts_table()
    return True

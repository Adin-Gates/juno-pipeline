from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem, QTextEdit, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from juno.paths import list_shows, get_show_title, list_sequences, list_shots
from juno.config import shot_resolver
from juno.scaffolding import scaffold_show
import json

class ShowCreator(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create New Show")
        self.show_code_label = QLabel("Enter new show code")
        self.show_code_line = QLineEdit()
        self.title_label = QLabel("Enter new show title")
        self.title_line = QLineEdit()
        self.submit_button = QPushButton("Submit")
        self.feedback_field = QLabel()
        self.done_button = QPushButton("Done")

        self.submit_button.clicked.connect(self.on_submit_button_clicked)
        self.done_button.clicked.connect(self.on_done_button_clicked)

        self.feedback_field.setText(f"Ready.")

        layout = QVBoxLayout()
        layout.addWidget(self.show_code_label)
        layout.addWidget(self.show_code_line)
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_line)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.feedback_field)
        layout.addWidget(self.done_button)

        self.setLayout(layout)


    def on_done_button_clicked(self):
        self.close()


    def on_submit_button_clicked(self):

        show_code = self.show_code_line.text().strip()
        title = self.title_line.text()

        if not show_code.strip():
            self.feedback_field.setText(f"Please enter a show code.")
            return

        if not title.strip():
            self.feedback_field.setText(f"Please enter a title.")
            return

        try:
            scaffold_show(show_code, title)
            self.feedback_field.setText(f"Created new show {show_code}.")

        except FileExistsError:
            self.feedback_field.setText(f"Show already exists.")
            QMessageBox.warning(self, "Error", "Show already exists. Please use code not used by another show.")
            







if __name__ == "__main__":

    app = QApplication([])
    creator = ShowCreator()
    creator.show()
    app.exec()
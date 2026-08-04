from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem, QTextEdit, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from juno.paths import list_shows, get_show_title, list_sequences, list_shots
from juno.config import shot_resolver
from juno.scaffolding import scaffold_show, scaffold_sequence, scaffold_shot
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

        self.submit_button.clicked.connect(self.on_show_submit_button_clicked)
        self.done_button.clicked.connect(self.on_show_done_button_clicked)

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


    def on_show_done_button_clicked(self):
        self.close()


    def on_show_submit_button_clicked(self):

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

        except ValueError:
            self.feedback_field.setText(f"Show code empty.")
            QMessageBox.warning(self, "Error", "Show code is empty.")
            

class SequenceCreator(QWidget):

    def __init__(self, show_code):
        super().__init__()

        self.show_code = show_code

        self.setWindowTitle("Create New Sequence")
        self.show_code_label = QLabel(f"[{self.show_code}] is the currently selected show.")
        self.sequence_code_label = QLabel("Enter new sequence code")
        self.sequence_code_line = QLineEdit()
        self.submit_button = QPushButton("Submit")
        self.feedback_field = QLabel()
        self.done_button = QPushButton("Done")



        self.submit_button.clicked.connect(self.on_sequence_submit_button_clicked)
        self.done_button.clicked.connect(self.on_sequence_done_button_clicked)

        self.feedback_field.setText(f"Ready.")

        layout = QVBoxLayout()
        layout.addWidget(self.show_code_label)
        layout.addWidget(self.sequence_code_label)
        layout.addWidget(self.sequence_code_line)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.feedback_field)
        layout.addWidget(self.done_button)

        self.setLayout(layout)



    def on_sequence_done_button_clicked(self):
        self.close()


    def on_sequence_submit_button_clicked(self):

        sequence_code = self.sequence_code_line.text().strip()

        if not sequence_code.strip():
            self.feedback_field.setText(f"Please enter a sequence code.")
            return

        try:
            scaffold_sequence(self.show_code,sequence_code)
            self.feedback_field.setText(f"Created new sequence [{sequence_code}] in {self.show_code}.")

        except FileNotFoundError:
            self.feedback_field.setText(f"Show does not exists.")
            QMessageBox.warning(self, "Error", "The show where sequence is being created does not exist.")

        except FileExistsError:
            self.feedback_field.setText(f"Sequence already exists.")
            QMessageBox.warning(self, "Error", "Sequence already exists. Please use sequence name not already in use.")

        except ValueError:
            self.feedback_field.setText(f"Sequence code empty.")
            QMessageBox.warning(self, "Error", "Sequence code is empty.")





class ShotCreator(QWidget):

    def __init__(self, show_code, sequence_code):
        super().__init__()

        self.show_code = show_code
        self.sequence_code = sequence_code

        self.setWindowTitle("Create New Shot")
        self.show_code_label = QLabel(f"[{self.show_code}] is the currently selected show.")
        self.sequence_code_label = QLabel(f"[{self.sequence_code}] is the currently selected sequence.")

        self.shot_code_label = QLabel("Enter new shot code")
        self.shot_code_line = QLineEdit()
        self.submit_button = QPushButton("Submit")
        self.feedback_field = QLabel()
        self.done_button = QPushButton("Done")



        self.submit_button.clicked.connect(self.on_shot_submit_button_clicked)
        self.done_button.clicked.connect(self.on_shot_done_button_clicked)

        self.feedback_field.setText(f"Ready.")

        layout = QVBoxLayout()
        layout.addWidget(self.show_code_label)
        layout.addWidget(self.sequence_code_label)
        layout.addWidget(self.shot_code_label)
        layout.addWidget(self.shot_code_line)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.feedback_field)
        layout.addWidget(self.done_button)

        self.setLayout(layout)



    def on_shot_done_button_clicked(self):
        self.close()


    def on_shot_submit_button_clicked(self):

        shot_code = self.shot_code_line.text().strip()

        if not shot_code.strip():
            self.feedback_field.setText(f"Please enter a shot code.")
            return

        try:
            scaffold_shot(self.show_code,self.sequence_code,shot_code)
            self.feedback_field.setText(f"Created new shot [{shot_code}] in {self.show_code} sequence {self.sequence_code}.")

        except FileNotFoundError:
            self.feedback_field.setText(f"Show or sequence does not exists.")
            QMessageBox.warning(self, "Error", "The show or sequence where shot is being created does not exist.")

        except FileExistsError:
            self.feedback_field.setText(f"Shot already exists.")
            QMessageBox.warning(self, "Error", "Shot already exists. Please use shot name not already in use.")







if __name__ == "__main__":

    app = QApplication([])
    creator = SequenceCreator("BOBO")
    creator.show()
    app.exec()
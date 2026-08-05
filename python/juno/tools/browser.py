from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem, QTextEdit, QPushButton
from PySide6.QtCore import Qt
from juno.paths import list_shows, get_show_title, list_sequences, list_shots
from juno.config import shot_resolver
from juno.tools.creator import ShowCreator, SequenceCreator, ShotCreator
import json

class JunoBrowser(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Juno Browser")

        self.show_list_widget = QListWidget()
        self.sequence_list_widget = QListWidget()
        self.shot_list_widget = QListWidget()
        self.config_display = QTextEdit()
        self.config_display.setReadOnly(True)
        self.add_show_button = QPushButton("+")
        self.add_sequence_button = QPushButton("+")
        self.add_shot_button = QPushButton("+")

        self.current_show = None
        self.current_sequence = None
        self.current_shot = None

        for show_code in list_shows():
            title = get_show_title(show_code)
            item = QListWidgetItem(f"[{show_code}] - {title}")
            item.setData(Qt.UserRole, show_code)
            self.show_list_widget.addItem(item)

        self.show_list_widget.itemClicked.connect(self.on_show_clicked)
        self.sequence_list_widget.itemClicked.connect(self.on_sequence_clicked)
        self.shot_list_widget.itemClicked.connect(self.on_shot_clicked)
        self.add_show_button.clicked.connect(self.on_add_show_clicked)
        self.add_sequence_button.clicked.connect(self.on_add_sequence_clicked)
        self.add_shot_button.clicked.connect(self.on_add_shot_clicked)

        self.add_sequence_button.setEnabled(False)
        self.add_shot_button.setEnabled(False)

        show_column = QVBoxLayout()
        show_column.addWidget(self.show_list_widget)
        show_column.addWidget(self.add_show_button)

        sequence_column = QVBoxLayout()
        sequence_column.addWidget(self.sequence_list_widget)
        sequence_column.addWidget(self.add_sequence_button)

        shot_column = QVBoxLayout()
        shot_column.addWidget(self.shot_list_widget)
        shot_column.addWidget(self.add_shot_button)

        config_column = QVBoxLayout()
        config_column.addWidget(self.config_display)


        main_layout = QHBoxLayout()
        main_layout.addLayout(show_column)
        main_layout.addLayout(sequence_column)
        main_layout.addLayout(shot_column)
        main_layout.addLayout(config_column)


        self.setLayout(main_layout)



    def on_show_clicked(self, item):

        print("You clicked:", item.text())

        show_code = item.data(Qt.UserRole)
        self.current_show = show_code
        self.sequence_list_widget.clear()
        self.shot_list_widget.clear()
        self.config_display.clear()

        sequences = list_sequences(show_code)

        self.add_shot_button.setEnabled(False)
        self.add_sequence_button.setEnabled(True)

        for seq in sequences:
            i = QListWidgetItem(f"{seq}")
            i.setData(Qt.UserRole, seq)
            self.sequence_list_widget.addItem(i)


    def on_sequence_clicked(self, item):
        print("You clicked:", item.text())

        show_code = self.current_show
        sequence_code = item.data(Qt.UserRole)

        self.current_sequence = sequence_code
        self.shot_list_widget.clear()
        self.config_display.clear()

        shots = list_shots(show_code, sequence_code)

        self.add_shot_button.setEnabled(True)

        for shot in shots:
            i = QListWidgetItem(f"{shot}")
            i.setData(Qt.UserRole, shot)
            self.shot_list_widget.addItem(i)


    def on_shot_clicked(self, item):

        shot_code = item.data(Qt.UserRole)
        self.current_shot = shot_code

        print("You clicked:", shot_code)

        config_data = shot_resolver(self.current_show,self.current_sequence,self.current_shot)
        config_readable = json.dumps(config_data, indent=2)

        self.config_display.setPlainText(config_readable)


    def refresh_shows(self):
        self.show_list_widget.clear()
        for show_code in list_shows():
            title = get_show_title(show_code)
            item = QListWidgetItem(f"[{show_code}] - {title}")
            item.setData(Qt.UserRole, show_code)
            self.show_list_widget.addItem(item)


    def refresh_sequences(self):
        self.sequence_list_widget.clear()
        for seq in list_sequences(self.current_show):
            item = QListWidgetItem(seq)
            item.setData(Qt.UserRole, seq)
            self.sequence_list_widget.addItem(item)

    def refresh_shots(self):
        self.shot_list_widget.clear()
        for shot in list_shots(self.current_show, self.current_sequence):
            i = QListWidgetItem(f"{shot}")
            i.setData(Qt.UserRole, shot)
            self.shot_list_widget.addItem(i)

    
    def on_add_show_clicked(self):
        self.show_creator = ShowCreator()
        self.show_creator.created.connect(self.refresh_shows)
        self.show_creator.show()

    def on_add_sequence_clicked(self):
        self.sequence_creator = SequenceCreator(self.current_show)
        self.sequence_creator.created.connect(self.refresh_sequences)
        self.sequence_creator.show()

    def on_add_shot_clicked(self):
        self.shot_creator = ShotCreator(self.current_show, self.current_sequence)
        self.shot_creator.created.connect(self.refresh_shots)
        self.shot_creator.show()







if __name__ == "__main__":

    app = QApplication([])
    browser = JunoBrowser()
    browser.show()
    app.exec()
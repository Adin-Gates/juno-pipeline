from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem, QTextEdit
from PySide6.QtCore import Qt
from juno.paths import list_shows, get_show_title, list_sequences, list_shots
from juno.config import shot_resolver
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


        layout = QHBoxLayout()
        layout.addWidget(self.show_list_widget)
        layout.addWidget(self.sequence_list_widget)
        layout.addWidget(self.shot_list_widget)
        layout.addWidget(self.config_display)

        self.setLayout(layout)



    def on_show_clicked(self, item):

        print("You clicked:", item.text())

        show_code = item.data(Qt.UserRole)
        self.current_show = show_code
        self.sequence_list_widget.clear()

        sequences = list_sequences(show_code)

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

        shots = list_shots(show_code, sequence_code)

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

        



if __name__ == "__main__":

    app = QApplication([])
    browser = JunoBrowser()
    browser.show()
    app.exec()
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox,
    QComboBox, QFileDialog, QFrame, QMessageBox
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QDragEnterEvent, QDropEvent, QIcon
from PyQt5.QtCore import Qt, QMimeData


class VideoProcessingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SupFrame")
        self.setFixedSize(338, 634)

        # Set background image
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("background.png")))  # Replace with your image path
        self.setPalette(palette)

        # set icon
        self.setWindowIcon(QIcon('icon.png'))

        # Main layout
        layout = QVBoxLayout()

        # Video drop area
        self.video_drop_area = QFrame(self)
        self.video_drop_area.setStyleSheet("background-color: #23989d;")
        self.video_drop_area.setAcceptDrops(True)
        self.video_drop_area.setFixedHeight(100)
        layout.addWidget(self.video_drop_area)

        # De-noise option
        self.denoise_checkbox = QCheckBox("De-noise")
        self.denoise_checkbox.setStyleSheet("background: transparent;")
        layout.addWidget(self.denoise_checkbox)

        # Super-resolution option
        self.superres_checkbox = QCheckBox("Super-resolution")
        self.superres_checkbox.setStyleSheet("background: transparent;")
        layout.addWidget(self.superres_checkbox)

        # Filter method dropdown
        self.filter_method_combo = QComboBox()
        self.filter_method_combo.addItems(["Color blindness pattern", "Monochrome", "Eye protection"])
        filter_label = QLabel("Choose filter method")
        filter_label.setStyleSheet("background: transparent;")
        layout.addWidget(filter_label)
        layout.addWidget(self.filter_method_combo)

        # Model selection dropdown
        self.model_combo = QComboBox()
        self.model_combo.addItems(["Transformer", "CNN", "GAN"])
        model_label = QLabel("Select model")
        model_label.setStyleSheet("background: transparent;")
        layout.addWidget(model_label)
        layout.addWidget(self.model_combo)

        # Output path specification
        output_path_label = QLabel("Specify your output path")
        output_path_label.setStyleSheet("background: transparent;")
        layout.addWidget(output_path_label)

        self.output_path_button = QPushButton("Choose output path")
        self.output_path_button.clicked.connect(self.choose_output_path)
        layout.addWidget(self.output_path_button)

        # Please wait label
        self.wait_label = QLabel("Please waiting for a few minutes ")
        self.wait_label.setStyleSheet("background: transparent;")
        layout.addWidget(self.wait_label)

        # Action buttons
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_all)
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm_action)

        # Button layout
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.confirm_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.show()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.preview_video(file_path)
            return file_path  # video file path

    def choose_output_path(self):
        output_path, _ = QFileDialog.getSaveFileName(self, "Choose Output Path")
        if output_path:
            print(f"Selected output path: {output_path}")
            return output_path  # output path

    def clear_all(self):  # clear all chooses
        self.denoise_checkbox.setChecked(False)
        self.superres_checkbox.setChecked(False)
        self.filter_method_combo.setCurrentIndex(0)
        self.model_combo.setCurrentIndex(0)

    def confirm_action(self):
        # Implement your action confirmation logic here
        QMessageBox.information(self, "Info", "Processing started!")

    def preview_video(self, file_path):
        # Implement your video preview logic here
        print(f"Previewing video: {file_path}")


def run_app():
    app = QApplication(sys.argv)
    ex = VideoProcessingApp()
    sys.exit(app.exec_())


run_app()
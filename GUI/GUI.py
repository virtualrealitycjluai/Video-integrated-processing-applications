import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox,
    QComboBox, QFileDialog, QFrame, QMessageBox, QLineEdit
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon
from PyQt5.QtCore import Qt, pyqtSignal


class Windows(QWidget):
    values_confirmed = pyqtSignal(bool, bool, str, str, str, str, str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SupFrame")
        self.setFixedSize(338, 634)

        # Set background image and icon
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("GUI/background.png")))
        self.setPalette(palette)
        self.setWindowIcon(QIcon('GUI/icon.png'))

        # Main layout
        layout = QVBoxLayout()
        # 增加输入框，输入目标帧率
        # Video path label
        self.frame_in = QLabel("Frame interpolation")
        self.video_path_label = QLabel("Select your video path")
        self.video_path_label.setStyleSheet("background-color: transparent;")
        layout.addWidget(self.video_path_label)

        # Button to choose video path
        self.video_path_button = QPushButton("Choose video path")
        self.video_path_button.clicked.connect(self.choose_video_path)
        layout.addWidget(self.video_path_button)

        # De-noise and Super-resolution options
        self.denoise_checkbox = QCheckBox("De-noise")
        self.superres_checkbox = QCheckBox("Super-resolution")
        layout.addWidget(self.denoise_checkbox)
        layout.addWidget(self.superres_checkbox)

        # Super-resolution scale options (x2, x3, x4)
        self.superres_scale_combo = QComboBox()
        self.superres_scale_combo.addItems(["x2", "x3", "x4"])
        layout.addWidget(QLabel("Select super-resolution scale"))
        layout.addWidget(self.superres_scale_combo)

        # Filter method dropdown
        self.filter_method_combo = QComboBox()
        self.filter_method_combo.addItems(["", "Color blindness pattern", "Monochrome", "Eye protection"])
        layout.addWidget(QLabel("Choose filter method"))
        layout.addWidget(self.filter_method_combo)

        # Model selection dropdown
        self.model_combo = QComboBox()
        self.model_combo.addItems(["", "Transformer", "UNet-3D"])
        layout.addWidget(QLabel("Select model"))
        layout.addWidget(self.model_combo)

        # Target frame rate input box
        self.frame_rate_input = QLineEdit()
        self.frame_rate_input.setPlaceholderText("Enter target frame rate")
        layout.addWidget(QLabel("Enter target frame rate"))
        layout.addWidget(self.frame_rate_input)

        # Output path button
        self.output_path_button = QPushButton("Choose output path")
        self.output_path_button.clicked.connect(self.choose_output_path)
        layout.addWidget(QLabel("Specify your output path"))
        layout.addWidget(self.output_path_button)

        # Action buttons
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_all)
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm_action)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.confirm_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def choose_video_path(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self, "Choose Video Path", "", "Videos (*.mp4 *.avi *.mov)")
        if self.video_path:
            self.video_path_label.setText(f"Selected: {self.video_path}")

    def choose_output_path(self):
        self.output_path = QFileDialog.getExistingDirectory(self, "Choose Output Directory")

    def clear_all(self):
        self.denoise_checkbox.setChecked(False)
        self.superres_checkbox.setChecked(False)
        self.filter_method_combo.setCurrentIndex(0)
        self.model_combo.setCurrentIndex(0)
        self.superres_scale_combo.setCurrentIndex(0)
        self.frame_rate_input.setText('')
        self.video_path = ''
        self.output_path = ''
        self.video_path_label.setText("Select your video path")  # Reset the video path label

    def confirm_action(self):
        denoise = self.denoise_checkbox.isChecked()
        superres = self.superres_checkbox.isChecked()
        filter_method = self.filter_method_combo.currentText()
        model = self.model_combo.currentText()
        output_path = getattr(self, 'output_path', '')
        video_path = getattr(self, 'video_path', '')
        superres_scale = self.superres_scale_combo.currentText()  # 获取超分倍率
        frame_rate = self.frame_rate_input.text()  # 使用 .text() 获取帧率输入

        self.values_confirmed.emit(
            denoise, superres, filter_method, model,
            output_path, video_path, superres_scale, frame_rate
        )
        QMessageBox.information(self, "Info", "Processing started!")


def run_app(confirm=None):
    app = QApplication(sys.argv)
    window = Windows()

    # Connect the signal to the provided handler if it exists
    if confirm:
        window.values_confirmed.connect(confirm)

    window.show()
    app.exec_()
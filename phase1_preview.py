import sys
import os
from datetime import datetime
from picamera2 import Picamera2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel,
    QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QStatusBar
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap


SAVE_FOLDER = os.path.expanduser("~/microscope_captures")
os.makedirs(SAVE_FOLDER, exist_ok=True)


class MicroscopeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Microscope Viewer")
        self.setMinimumSize(800, 600)

        # --- Camera setup ---
        self.camera = Picamera2()
        config = self.camera.create_preview_configuration(
            main={"size": (640, 480), "format": "RGB888"}
        )
        self.camera.configure(config)
        self.camera.start()

        # --- Preview label ---
        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        self.image_label.setMinimumSize(640, 480)

        # --- Capture button ---
        self.capture_btn = QPushButton("Capture Image")
        self.capture_btn.setFixedHeight(50)
        self.capture_btn.clicked.connect(self.capture_image)

        # --- Layout ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.capture_btn)
        btn_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(btn_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # --- Status bar at bottom ---
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")

        # --- Timer: 30fps preview ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)

    def update_frame(self):
        frame = self.camera.capture_array()
        h, w, ch = frame.shape
        qt_image = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))
        # Store latest frame for saving
        self.latest_frame = frame

    def capture_image(self):
        if not hasattr(self, 'latest_frame'):
            self.status.showMessage("No frame yet, try again")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.jpg"
        filepath = os.path.join(SAVE_FOLDER, filename)

        # Use picamera2 to save a full quality still
        self.timer.stop()
        self.camera.stop()

        still_config = self.camera.create_still_configuration()
        self.camera.configure(still_config)
        self.camera.start()
        self.camera.capture_file(filepath)
        self.camera.stop()

        # Restart preview
        preview_config = self.camera.create_preview_configuration(
            main={"size": (640, 480), "format": "RGB888"}
        )
        self.camera.configure(preview_config)
        self.camera.start()
        self.timer.start(33)

        self.status.showMessage(f"Saved: {filepath}")

    def closeEvent(self, event):
        self.timer.stop()
        self.camera.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MicroscopeApp()
    window.show()
    sys.exit(app.exec_())

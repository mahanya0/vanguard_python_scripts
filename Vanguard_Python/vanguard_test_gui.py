import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QTimer
from test_firmata import status_updater, start_arduino_in_background
from PyQt5.QtMultimedia import QCamera, QCameraInfo
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QGridLayout, QProgressBar
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class IRSensorDisplay(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("IR Sensor Data Display")
        self.setGeometry(100, 100, 300, 200)

        # Set up a label to display the IR sensor data
        self.sensor_label = QLabel("IR Sensor Data: --", self)
        self.sensor_label.setStyleSheet("font-size: 18px;")
        
        # Arrange the label in a layout
        layout = QGridLayout()
        layout.addWidget(self.sensor_label)

        # Set up the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # List to store camera objects
        self.cameras = []
        
        # Set up available cameras
        webcams = QCameraInfo.availableCameras()  # List of available cameras
        if webcams:
            for index, webcam_info in enumerate(webcams):
                # Create a label for each webcam feed
                #layout.addWidget(QLabel(f"Webcam {index + 1} Feed:"), index, 0)
                layout.addWidget(QLabel(f"Webcam {index + 1} Feed:"), index, 0, Qt.AlignCenter)

                # Create a viewfinder for each webcam
                feed = QCameraViewfinder(self)
                layout.addWidget(feed, index, 1)
                
                # Initialize camera and set the viewfinder
                camera = QCamera(webcam_info)
                camera.setViewfinder(feed)
                camera.start()
                
                # Store the camera object to keep it active
                self.cameras.append(camera)


        # Connect the status_changed signal to the update_sensor_data method
        status_updater.status_changed.connect(self.update_sensor_data)

        # Start the Arduino communication in the background
        start_arduino_in_background()

    def update_sensor_data(self, new_status):
        # Update the label with the new data from the signal
        self.sensor_label.setText(f"IR Sensor Data: {new_status}")

def main():
    app = QApplication(sys.argv)
    window = IRSensorDisplay()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

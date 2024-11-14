from pyfirmata2 import Arduino, util
from time import sleep
import threading
from PyQt5.QtCore import QObject, pyqtSignal

# Initialize the Arduino board with the correct port
board = Arduino("COM10")  # Replace with your device path, e.g., "COM10" or "/dev/ttyUSB0"

board.digital[9].mode = 0  # Set pin 9 as input
obstacle_pin_number = 9

# Create a class to emit status updates
class StatusUpdater(QObject):
    status_changed = pyqtSignal(str)  # Define a signal that carries a string

    def __init__(self):
        super().__init__()
        self.status = "Clear"

    def update_status(self, data):
        # Update status based on sensor data and emit the change
        if data:
            new_status = "Clear"
        else:
            new_status = "Obstacle"
        
        if new_status != self.status:
            self.status = new_status
            self.status_changed.emit(self.status)  # Emit the updated status
            print(self.status, "|| RAW SENSOR DATA: ", data)

# Instantiate the status updater
status_updater = StatusUpdater()

def obstacle_callback(data):
    # Update the status through the status updater
    status_updater.update_status(data)

def start_arduino():
    # Register the callback on the digital pin
    board.digital[obstacle_pin_number].register_callback(obstacle_callback)

    # Enable reporting for the digital pin
    board.digital[obstacle_pin_number].enable_reporting()

    # Start the iterator to continuously read data
    it = util.Iterator(board)
    it.start()

    # Run indefinitely to keep reading data
    while True:
        sleep(1)

# Start the Arduino communication in a background thread
def start_arduino_in_background():
    arduino_thread = threading.Thread(target=start_arduino, daemon=True)
    arduino_thread.start()

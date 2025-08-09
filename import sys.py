import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

def on_button_click():
    print("You clicked the button!")

app = QApplication(sys.argv)

# Create main window
window = QWidget()
window.setWindowTitle("TriFlow Prototype - Day 1")

# Create a button
button = QPushButton("Click Me!")
button.clicked.connect(on_button_click)

# Layout
layout = QVBoxLayout()
layout.addWidget(button)
window.setLayout(layout)

window.show()
sys.exit(app.exec())


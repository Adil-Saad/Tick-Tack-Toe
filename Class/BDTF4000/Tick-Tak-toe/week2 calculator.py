import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QWidget, QGridLayout
from PyQt5.QtCore import Qt

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and geometry for a larger display
        self.setWindowTitle("Calculator")
        self.setGeometry(1000, 400, 600, 800)

        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Display widget
        self.display = QLineEdit(self)
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(100)
        main_layout.addWidget(self.display)

        # Buttons layout
        button_layout = QGridLayout()
        buttons = [
            '7', '8', '9', '/', 'C',  # Added 'C' for clear button
            '4', '5', '6', '*', 
            '1', '2', '3', '-', 
            '0', '.', '=', '+'
        ]

        row, col = 0, 0
        for button in buttons:
            button_obj = QPushButton(button)
            button_obj.setFixedSize(120, 120)  # Increase button size for larger display
            button_layout.addWidget(button_obj, row, col)
            button_obj.clicked.connect(self.on_click)
            col += 1
            if col > 4:  # Changed to 5 columns to accommodate the Clear button
                col = 0
                row += 1

        main_layout.addLayout(button_layout)

        # Container widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def on_click(self):
        button_text = self.sender().text()

        if button_text == '=':
            try:
                result = eval(self.display.text())
                self.display.setText(str(result))
            except:
                self.display.setText("Error")
        elif button_text == 'C':  # Clear the display when 'C' is clicked
            self.display.clear()
        else:
            self.display.setText(self.display.text() + button_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())

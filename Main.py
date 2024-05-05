import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
import requests

class CollegeDataApp(QWidget):
    def __init__(self):
        super().__init__()

        self.api_key = "HRnr80yWE4NsBtYUorM2hHu1EAhRYIIRJpqZ7eDa"
        self.state_input = QLineEdit()
        self.data_label = QLabel("")

        self.init_ui()

    def init_ui(self):
        # Layout
        main_layout = QVBoxLayout(self)
        input_layout = QHBoxLayout()

        # Input elements
        state_label = QLabel("State (optional):")
        get_data_button = QPushButton("Get College Data")

        # Connect button click to fetch data function
        get_data_button.clicked.connect(self.fetch_college_data)

        # Add elements to layouts
        input_layout.addWidget(state_label)
        input_layout.addWidget(self.state_input)
        input_layout.addWidget(get_data_button)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.data_label)

        self.setLayout(main_layout)
        self.setWindowTitle("College Data App")
        self.show()

    def fetch_college_data(self):
        state = self.state_input.text() if self.state_input.text() else ""
        params = {
            'school.state': state,
            'api_key': self.api_key
        }

        try:
            response = requests.get("https://api.data.gov/ed/collegescorecard/v1/schools?", params=params)
            data = response.json()
            self.display_data(data)
        except Exception as e:
            self.data_label.setText(f"Error fetching data: {e}")

    def display_data(self, data):
        college_data_text = ""
        for school in data['results']:
            school_name = school.get('school').get('name')
            school_state = school.get('school').get('state')
            # Add other data points as needed
            college_data_text += f"Name: {school_name}\nState: {school_state}\n\n"
        self.data_label.setText(college_data_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CollegeDataApp()
    sys.exit(app.exec())

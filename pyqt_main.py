import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QTextBrowser
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QUrl
import requests

class CollegeDataApp(QWidget):
    def __init__(self):
        super().__init__()

        self.api_key = "HRnr80yWE4NsBtYUorM2hHu1EAhRYIIRJpqZ7eDa"
        self.state_input = QLineEdit()
        self.degree_input = QLineEdit()
        self.college_list = QListWidget()
        self.details_view = QTextBrowser()

        self.init_ui()

    def init_ui(self):
        # Layout
        self.main_layout = QVBoxLayout(self)
        input_layout = QHBoxLayout()

        # Title
        self.title_label = QLabel("College Data App")
        self.title_label.setFont(QFont("Arial", 24))
        self.title_label.setStyleSheet("color: blue;")
        self.main_layout.addWidget(self.title_label)

        # Explanation
        self.explanation_label = QLabel("Search for colleges by state and degree level. Click on a college for more details.")
        self.explanation_label.setFont(QFont("Arial", 14))
        self.main_layout.addWidget(self.explanation_label)

        # Input elements
        state_label = QLabel("State (optional):")
        degree_label = QLabel("Degree Level (optional, e.g., 1,2):")
        get_data_button = QPushButton("Get College Data")

        # Apply style to input elements
        state_label.setStyleSheet("font-size: 18px;")
        degree_label.setStyleSheet("font-size: 18px;")
        get_data_button.setStyleSheet("font-size: 18px; padding: 5px 10px;")

        # Connect button click to fetch data function
        get_data_button.clicked.connect(self.fetch_college_data)

        # Add elements to layouts
        input_layout.addWidget(state_label)
        input_layout.addWidget(self.state_input)
        input_layout.addWidget(degree_label)
        input_layout.addWidget(self.degree_input)
        input_layout.addWidget(get_data_button)
        self.main_layout.addLayout(input_layout)
        self.main_layout.addWidget(self.college_list)
        self.main_layout.addWidget(self.details_view)

        # Apply style to college list
        self.college_list.setStyleSheet("font-size: 16px; border: 2px solid #ccc; border-radius: 5px; padding: 10px;")

        self.setLayout(self.main_layout)
        self.setWindowTitle("College Data App")
        self.show()

    def fetch_college_data(self):
        state = self.state_input.text() if self.state_input.text() else ""
        degree = self.degree_input.text() if self.degree_input.text() else "1,2"
        params = {
            'school.state': state,
            'school.degrees_awarded.predominant': degree,
            'api_key': self.api_key
        }

        try:
            response = requests.get("https://api.data.gov/ed/collegescorecard/v1/schools?", params=params)
            data = response.json()
            self.display_data(data)
        except Exception as e:
            self.college_list.addItem(QListWidgetItem(f"Error fetching data: {e}"))

    def display_data(self, data):
        self.college_list.clear()
        for school in data['results']:
            school_name = school.get('school').get('name')
            school_state = school.get('school').get('state')

            # Extract and format tuition data
            instate_tuition = school.get('latest').get('cost').get('tuition').get('in_state')
            outstate_tuition = school.get('latest').get('cost').get('tuition').get('out_of_state')
            instate_tuition_formatted = f"In-State Tuition: ${instate_tuition:.2f}" if instate_tuition else "In-State Tuition: Not Available"
            outstate_tuition_formatted = f"Out-of-State Tuition: ${outstate_tuition:.2f}" if outstate_tuition else "Out-of-State Tuition: Not Available"

            # Add college data with tuition information
            item = QListWidgetItem(f"{school_name} - {school_state}\n{instate_tuition_formatted}\n{outstate_tuition_formatted}")
            self.college_list.addItem(item)

            # Set a custom data role to store the school details
            item.setData(1000, school)

        self.college_list.itemClicked.connect(self.show_college_details)

    def show_college_details(self, item):
        school = item.data(1000)
        school_name = school.get('school').get('name')
        school_state = school.get('school').get('state')
        instate_tuition = school.get('latest').get('cost').get('tuition').get('in_state')
        outstate_tuition = school.get('latest').get('cost').get('tuition').get('out_of_state')
        instate_tuition_formatted = f"In-State Tuition: ${instate_tuition:.2f}" if instate_tuition else "In-State Tuition: Not Available"
        outstate_tuition_formatted = f"Out-of-State Tuition: ${outstate_tuition:.2f}" if outstate_tuition else "Out-of-State Tuition: Not Available"

        # Google search URL for the college
        google_search_url = f"https://www.google.com/search?q={school_name.replace(' ', '+')}"

        # Display college details in the QTextBrowser
        details_html = f"""
        <h2>{school_name} - {school_state}</h2>
        <p>{instate_tuition_formatted}</p>
        <p>{outstate_tuition_formatted}</p>
        <p><a href="{google_search_url}" style="color: blue; text-decoration: none;" target="_blank">Search on Google</a></p>
        """
        self.details_view.setHtml(details_html)

        # Make the link clickable
        self.details_view.setOpenExternalLinks(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CollegeDataApp()
    sys.exit(app.exec())

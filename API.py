# For general python dataFrame manipulation, aggregations, and plots.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# For handling API calls. 
from pprint import pprint
# For user-friendly data file access.
import os
import requests
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class CollegeSchoolFetcher:
    def __init__(self, api_key,):
        self.api_key = api_key
        self.base_url = "https://api.data.gov/ed/collegescorecard/v1/schools?"

    def fetch_college_data(self, state='', degree_levels='1,2'):
        params = {
            'school.state': state,
            'school.degrees_awarded.predominant': degree_levels,
            'api_key': self.api_key
        }

        response = requests.get(self.base_url, params=params)
        data = response.json()

        return data['results']

if __name__ == "__main__":
    api_key = "HRnr80yWE4NsBtYUorM2hHu1EAhRYIIRJpqZ7eDa"
    college_fetcher = CollegeSchoolFetcher(api_key)

    college_data = college_fetcher.fetch_college_data()

    for school in college_data:
        school_id = school.get('id')
        school_name = school.get('school').get('name')
        school_state = school.get('school').get('state')
        school_city = school.get('school').get('city')
        instate_tuition = school.get('latest').get('cost').get('tuition').get('in_state')
        outstate_tuition = school.get('latest').get('cost').get('tuition').get('out_of_state')

        print(f"School ID: {school_id}")
        print(f"Name: {school_name}")
        print(f"State: {school_state}")
        print(f"City: {school_city}")
        print(f"In-State Tuition: ${instate_tuition}")
        print(f"Out-of-State Tuition: ${outstate_tuition}")
        print("-" * 30)
MoodleClone

This is a web application built with Django and Python for an academic course project.
Table of Contents

    Introduction
    Features
    Installation
    Usage
    Contributing
    License

Introduction

MoodleClone is a web application designed to mimic some functionalities of Moodle. It is developed using the Django framework in Python.
Features

    User authentication and management
    Course creation and enrollment
    Assignment submission and grading
    Simple, intuitive interface

Installation

    Clone the repository:

    sh

git clone https://github.com/MarinoLucicRaguz/MoodleAppPythonDjango.git

Navigate to the project directory:

sh

cd MoodleAppPythonDjango

Create and activate a virtual environment:

sh

python -m venv env
source env/bin/activate   # On Windows use `env\Scripts\activate`

Install the dependencies:

sh

pip install -r requirements.txt

Apply migrations:

sh

python manage.py migrate

Run the development server:

sh

    python manage.py runserver

Usage

    Access the application:
        Open your web browser and navigate to http://127.0.0.1:8000/.

    User operations:
        Register a new account or log in with an existing one.
        Enroll in courses, submit assignments, and view grades.

Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.
License

This project is licensed under the MIT License. See the LICENSE file for details

# GrievanceBackend

This is a Django web application that supports the API for the Grievance Management System [The Grievance Backend app is built on Django Rest Framework].

## Getting Started

These instructions will help you set up and run the project locally on your machine for development and testing purposes.

### Prerequisites

Before you can run the app, make sure you have the following installed:

- Python (latest version)
- pip (Python package manager)
- Virtualenv (optional but recommended)

### Installation

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/Txuraz/GrievanceBackend.git
   ```
2. Navigate to the project directory:
    ```
    cd my-django-app
    ```
3. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
    ```
    venv\Scripts\activate
    ```
5. Install the project dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Apply database migrations:
   ```
   python manage.py migrate
   ```
7. Start the development server:
   ```
   python manage.py runserver
   ```
##Note:
If Mysql server is not working configure your database as you like in **Settings.py** file located in project main directory.

## Usage
Once the development server is running, you can access the Django app in your web browser at http://localhost:8000/.

## Deployment



## Contributing
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the MIT License - see the LICENSE file for details..

   


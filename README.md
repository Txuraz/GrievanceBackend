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
    cd GrievanceBackend
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
6. copy .env.example to .env
   ```
   cp .env.example .env
   ```
   edit and add your database information and secret key in .env:
   ```
   SECRET_KEY=your-actual-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   DB_NAME=txu
   DB_USER=txuraz
   DB_PASSWORD=actual-password
   DB_HOST=localhost
   DB_PORT=3306

   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-actual-email@gmail.com
   EMAIL_HOST_PASSWORD=your-actual-email-password
   MAIL_FROM_ADDRESS=your-actual-email@gmail.com
   ```
7. Apply database migrations:
   ```
   python manage.py migrate
   ```
8. seed Grievances and user
   ```
   python manage.py user_seeder
   python manage.py grievance_seeder
   ```
9. Start the development server:
   ```
   python manage.py runserver
   ```
##Note:
If Mysql server is not working configure your database as you like in **Settings.py** file located in project main directory.

## Usage
Once the development server is running, you can access the Django app in your web browser at http://localhost:8000/.



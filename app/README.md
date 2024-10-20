
# Medication Management and Timesheet Application

## Overview

This application is designed to help users manage their medications and generate schedules (timesheets) for when they should take their medications. It includes features for user management, medication handling, timesheet generation, and file handling. It also integrates with OpenAI's API to assist in processing unstructured data related to medications.

## Features

### User Management
- Users can create accounts, log in, and log out.
- User data includes attributes like username, email, password, and role (e.g., admin or regular user).
- Passwords are securely hashed using bcrypt for safe storage.

### Medication Management
- Users can add, update, delete, and retrieve medications.
- Medications have attributes such as name, contents, objective, side effects, and dosage schedule.
- Users can upload files containing medication information in `.pdf`, `.docx`, `.txt`, or `.md` formats, and the application will parse the data.

### Timesheet Management
- Timesheets help users manage their medication schedules over a specified time frame.
- Timesheets include medication details, dosage information, and scheduling requirements.
- Timesheets are generated using OpenAI's API, based on the user's provided medication information and scheduling requirements.

### File Handling
- Users can upload documents containing medication information.
- The application can extract text from files with extensions like `.pdf`, `.docx`, `.txt`, and `.md`.
- The extracted data is used to create structured medication information.

### Integration with OpenAI
- OpenAI's API is used to parse unstructured text data and generate structured medication information.
- It is also used to generate timesheets that specify when users should take their medications.

## Installation

### Prerequisites
- Python 3.12+
- MongoDB
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the configuration file:
   - Create a configuration file named `config.dev.ini` with the following sections:
     ```ini
     [Database]
     uri = mongodb://localhost:27017/
     name = medication_timesheet

     [OpenAI]
     api_key = your_openai_api_key_here
     ```

6. Run the application:
   ```bash
   python app.py
   ```

## Usage

### Endpoints
- **User Management**
  - `/auth/signup` - Create a new user.
  - `/auth/login` - Log in with username and password.
  - `/auth/logout` - Log out the current user.

- **Medication Management**
  - `/medications` - Add, update, delete, or retrieve medications.
  - `/medications/upload` - Upload a document to add medication information.

- **Timesheet Management**
  - `/timesheets` - Create, update, or retrieve timesheets for a user's medication schedule.

### File Handling
- The application supports file uploads for `.pdf`, `.docx`, `.txt`, and `.md` formats to extract medication information.

### Generating Timesheets
- After adding medications, users can generate timesheets to specify when they should take each medication during a specified period.

## Project Structure
- **controllers/**: Contains controllers for managing users, medications, and timesheets.
- **services/**: Provides services for file reading, OpenAI integration, and password encoding.
- **db/**: Handles database interaction with MongoDB.
- **model/**: Defines data models such as User, Medication, and Timesheet.

## Technologies Used
- **Python**: Main programming language.
- **Flask**: Web framework used for building REST APIs.
- **MongoDB**: Database used to store user, medication, and timesheet information.
- **OpenAI API**: Used for generating structured information from unstructured text.
- **bcrypt**: Used for securely hashing user passwords.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- [Flask](https://flask.palletsprojects.com/)
- [MongoDB](https://www.mongodb.com/)
- [OpenAI API](https://openai.com/api/)

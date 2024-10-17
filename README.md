# SUMSUB API Integration

This project provides a Django-based application for integrating with the SUMSUB API to manage applicant data and document uploads for verification.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Features

- Create applicants in the SUMSUB system
- Upload identity documents for verification
- Retrieve verification status of applicants

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.8 or later
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   
2. **Create and activate a virtual environment:**

##### You can use venv (Python's built-in virtual environment module) to create a virtual environment.

   ```bash
    python -m venv .venv
   ```

For Windows:

```bash
  .venv\Scripts\activate
```

For macOS/Linux:
```bash
source .venv/bin/activate
```

3. **install the requirements packages for the project:**

```bash
    pip install -r requirements.txt
```

4. **Create a .env file in the root directory of your project and add your SUMSUB API credentials and any other required environment variables:**

```makefile
SUMSUB_APP_TOKEN=your_app_token
SUMSUB_SECRET_KEY=your_secret_key
SUMSUB_TEST_BASE_URL=https://api.sumsub.com
```

5. **Run database migrations:**

Apply the migrations to set up your database:

```bash
python manage.py migrate
```
6. **Start the application**

```bash

python manage.py runserver
```

#### You should see output indicating that the server is running, usually at http://127.0.0.1:8000/.

### API Endpoints
```
You can access the following API endpoints (replace <base_url> with your local server URL):

Create Applicant: POST <base_url>/applicant/create/
Upload Document: POST <base_url>/applicant/upload-document/
Get Applicant Status: GET <base_url>/applicant/<applicant_id>/status/`
```

### License
This project is licensed under the MIT License. See the LICENSE file for more details.
# Bank Statement Extractor

## Overview
This project is a bank statement extraction system built with Flask in Python. It processes bank statements and extracts relevant information for analysis and reporting.

## Prerequisites
- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Bishwaprotapi/bank-statement-extractor.git
    cd bank-statement-extractor
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

5. Set up environment variables:
    ```sh
    cp .env.example .env
    # Edit .env with your configuration
    ```

## Usage

### Running the Application
To start the Flask application locally:
```sh
python app.py
```
or
```sh
flask run
```
The application will be available at `http://127.0.0.1:80/`.

### Running with Docker
Build and run using Docker:
```sh
docker build -t bank-statement-extractor .
docker run -p 80:80 bank-statement-extractor
```

## Features
- Bank statement processing
- Information extraction
- RESTful API endpoints
- Docker support for easy deployment
- Configurable through environment variables

## Project Structure
```
.
├── apidocs/          # API documentation
├── config/           # Configuration files
├── src/              # Source code
│   ├── controller/   # API controllers
│   └── routes/       # API routes
├── .gitignore
├── .env              # Environment variables
├── app.py            # Main application file
├── Dockerfile        # Docker configuration
├── README.md         # This file
└── requirements.txt  # Python dependencies
```

## Contributing
Contributions are welcome! Please fork the repository and create a new branch for your changes.

## License
This project is licensed under the MIT License.
```

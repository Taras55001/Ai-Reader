# Ai Reader app 📝

A Django project that incorporates a chatbot using a language model and supports reading PDF, DOCX, and TXT documents, allowing users to interact with the content within the documents.

## Features
Chatbot integration\
Support for reading PDF, DOCX, and TXT documents\
User interaction with document content through the chat interface

Python 3.10 is required


## Installation
Clone the repository:\
Copy code and run on terminal\
`git clone https://github.com/Taras55001/Ai-Reader`

navigate to project directory 
`cd chat`\
Install the required packages:\
Copy code and run on terminal\
`pip install -r requirements.txt`
## Configuration
This project build on posgreSQL\
The project is required secret keys:\
SECRET_KEY='sample of django secret key'\
DATABASE_NAME='your database name'\
DATABASE_USER='your database name'\
DATABASE_PASSWORD='your database password'\
DATABASE_HOST='your database host'\
DATABASE_PORT='database port'\
HUGGINGFACEHUB_API_TOKEN='api token from your huggingface.co'
## Usage
Explain how to run and use your Django project. Include any relevant commands and details about accessing the application.

Copy code and run on terminal\
`python manage.py runserver`\
Visit http://localhost:8000 in your web browser.


## License
MIT License
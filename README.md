# Ai Reader app 📝

A Django project that incorporates a chatbot using a language model and supports reading PDF, DOCX, and TXT documents, allowing users to interact with the content within the documents.
LLM models used:
for answer generation - mistral ai/Mixtral-8x7B-Instruct-v0.1
for word embeddings context creation - all-MiniLM-L6-v2
vector database - FAISS

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
The project is required secret keys\
make new .env file in project directory\
put this keys into .env and replace values:
`SECRET_KEY='sample of django secret key'
DATABASE_NAME='your database name'
DATABASE_USER='your database name'
DATABASE_PASSWORD='your database password'
DATABASE_HOST='your database host'
DATABASE_PORT='database port'
HUGGINGFACEHUB_API_TOKEN='api token from your huggingface.co'`

Copy code and run on terminal\
`python manage.py runserver`\
Visit http://localhost:8000 in your web browser.
## Usage
Now you can use web site.Create user account and drop your files to make chat with LLM model

## License
MIT License
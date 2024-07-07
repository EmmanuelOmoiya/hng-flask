from dotenv import load_dotenv
import os

load_dotenv()

jwt = {
    "secret": os.getenv('JWT_SECRET'),
    "location": os.getenv('JWT_TOKEN_LOCATION')
}

app = {
    "port": os.getenv('PORT'),
    "secret": os.getenv('SECRET_KEY')
}

db = {
    "username": os.getenv('DB_USERNAME'),
    "password": os.getenv('DB_PASSWORD')
}
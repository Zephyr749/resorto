import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    DB_NAME = os.getenv('DB_NAME', 'resorto')
    JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-this')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRATION_DAYS = int(os.getenv('JWT_EXPIRATION_DAYS', 7))
    
    # Razorpay Configuration
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')

config = Config()

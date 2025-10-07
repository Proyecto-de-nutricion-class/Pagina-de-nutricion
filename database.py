# Contenido de database.py
from pymongo import MongoClient
import os 
from dotenv import load_dotenv 

# Carga variables de entorno (para pruebas locales con .env)
load_dotenv()

# Lee la variable de entorno. En Docker será 'mongodb://mongo:27017/'
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/") 
DATABASE_NAME = "medical_db"

client = None
medical_histories_collection = None

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping') 
    db = client[DATABASE_NAME]
    medical_histories_collection = db["histories"]
    print(f"Conexión exitosa a MongoDB en: {MONGO_URI}")
except Exception as e:
    print(f"Error de conexión a MongoDB: {e}")
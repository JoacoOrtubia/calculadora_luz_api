from app.main import app
import sys
import os

# agrega el path del proyecto para que Python encuentre el paquete app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# main.py
import sys
import os

# Agregar el directorio actual al path para importaciones
sys.path.append(os.path.dirname(__file__))

from interfaz import InterfazRefraccion
import customtkinter as ctk

if __name__ == "__main__":
    app = InterfazRefraccion()
    app.mainloop()
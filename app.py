from flask import Flask, render_template, request
from markupsafe import escape # La función escape ahora se importa desde aquí
def create_app():
    app = Flask(__name__) # Inicializamos la aplicación Flask
    @app.route('/Wordle') # Definimos una ruta para la página principal
    def home():
        try:
            with open('Game/Wordle.txt', 'r', encoding='utf-8') as f:
                content = f.read()
                # Usamos la etiqueta <pre> para preservar los saltos de línea y espacios.
                # Usamos escape() por seguridad, para evitar que se interprete HTML del archivo.
                return f"<pre>{escape(content)}</pre>"
        except FileNotFoundError:
            return "El archivo 'code.txt' no fue encontrado."
    return app


if __name__ == '__main__': # Punto de entrada de la aplicación 
   app = create_app() # Creamos la aplicación
   app.run() # Ejecutamos la aplicación
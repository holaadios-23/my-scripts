import os
from flask import Flask, send_from_directory, abort
from markupsafe import escape

# Directorio que queremos compartir. Por seguridad, el servidor solo tendrá acceso a esta carpeta.
SHARE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'texts'))

def create_app():
    app = Flask(__name__) # Inicializamos la aplicación Flask

    @app.route('/', defaults={'subpath': ''})
    @app.route('/<path:subpath>')
    def serve(subpath):
        # Construimos la ruta completa y segura al archivo/directorio solicitado
        abs_path = os.path.join(SHARE_DIR, subpath)

        # Verificamos que la ruta solicitada no se salga del directorio compartido (seguridad)
        if not abs_path.startswith(SHARE_DIR):
            abort(400, "Petición inválida.")

        # Si la ruta es un directorio, mostramos su contenido
        if os.path.isdir(abs_path):
            files = os.listdir(abs_path)
            html = f'<h1>/{escape(subpath)}</h1>'
            html += '<ul>'
            # Enlace para subir al directorio padre (si no estamos en la raíz)
            if subpath:
                parent_path = os.path.dirname(subpath)
                html += f'<li><a href="/{parent_path}">.. (Subir)</a></li>'
            
            for f in sorted(files):
                # Añadimos una barra al final si es un directorio
                display_name = f + '/' if os.path.isdir(os.path.join(abs_path, f)) else f
                html += f'<li><a href="/{os.path.join(subpath, f)}">{escape(display_name)}</a></li>'
            html += '</ul>'
            return html

        # Si la ruta es un archivo, lo mostramos en el navegador (o lo descarga si el navegador no puede mostrarlo)
        if os.path.isfile(abs_path):
            directory, filename = os.path.split(abs_path)
            return send_from_directory(directory, filename, as_attachment=False)
        
        # Si no se encuentra, devolvemos un error 404
        try:
            return abort(404)
        except Exception as e:
            return str(e)

    return app

if __name__ == '__main__': # Punto de entrada de la aplicación 
   app = create_app() # Creamos la aplicación
   # Usamos host='0.0.0.0' para que sea accesible desde otros dispositivos en la misma red
   app.run(host='0.0.0.0', port=5000, debug=True)

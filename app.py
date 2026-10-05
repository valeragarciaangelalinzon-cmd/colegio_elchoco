from flask import Flask
from controllers.apoderado_controller import apoderado_bp
from controllers.alumno_controller import alumno_bp
from controllers.matricula_controller import matricula_bp

app = Flask(__name__)

# Registrar los Controladores (Blueprints)
app.register_blueprint(apoderado_bp)
app.register_blueprint(alumno_bp)
app.register_blueprint(matricula_bp)

if __name__ == '__main__':
    app.run(debug=True)
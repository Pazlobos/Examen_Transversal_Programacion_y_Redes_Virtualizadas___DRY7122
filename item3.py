# item3.py
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)

# Configuración estricta de la base de datos SQLite local en la VM
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'usuarios.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy pasándole la app directamente
db = SQLAlchemy(app)

# Modelo de la Base de Datos para el examen (Mapeo de la tabla de usuarios)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

# Inicializar Base de Datos e Inyectar los integrantes reales de tu grupo
def inicializar_db():
    with app.app_context():
        db.create_all()
        
        # === INTEGRANTES DEL GRUPO REALES ===
        integrantes = ["maria_lobos", "tomas_sandretti", "johans_coye"]
        
        for integrante in integrantes:
            usuario_existente = Usuario.query.filter_by(nombre=integrante).first()
            if not usuario_existente:
                # Contraseña de ejemplo obligatoria para la prueba (puedes cambiarla si deseas)
                password_plana = "Duoc2026!"
                
                # Crear el HASH seguro requerido utilizando bcrypt (Rúbrica de Evaluación)
                salt = bcrypt.gensalt()
                hashed_pw = bcrypt.hashpw(password_plana.encode('utf-8'), salt).decode('utf-8')
                
                nuevo_usuario = Usuario(nombre=integrante, password_hash=hashed_pw)
                db.session.add(nuevo_usuario)
                
        db.session.commit()
        print("[OK] Base de datos 'usuarios.db' creada con éxito.")
        print("[OK] Integrantes cargados de forma segura con hashes encriptados.")

# Ruta de Login que validará a través de peticiones POST los usuarios y hashes correspondientes
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Faltan datos en formato JSON"}), 400
        
    username = data.get('username')
    password = data.get('password')
    
    # Buscar el usuario de forma respectiva en la BD SQL
    usuario = Usuario.query.filter_by(nombre=username).first()
    
    # Comparación segura del hash mediante la librería bcrypt
    if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
        return jsonify({"status": "success", "message": f"Bienvenido integrante {username}!"}), 200
    else:
        return jsonify({"status": "error", "message": "Credenciales incorrectas o no es miembro del examen"}), 401

if __name__ == "__main__":
    inicializar_db()
    print("\nServidor Flask iniciado de forma correcta.")
    print("Escuchando peticiones en el puerto obligatorio: 5800")
    # Ejecución obligatoria en el puerto 5800 solicitado en la evaluación
    app.run(host='0.0.0.0', port=5800, debug=True)
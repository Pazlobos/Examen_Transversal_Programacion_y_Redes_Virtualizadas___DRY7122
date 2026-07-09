from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Examen Transversal - Redes</h1><p>Integrantes del grupo: Lobos, San...</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
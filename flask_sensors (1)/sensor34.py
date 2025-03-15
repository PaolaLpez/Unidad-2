from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'vale',
    'password': '@Valeria-3211@*',
    'database': 'io2'
}

@app.route('/sensor34', methods=['POST'])
def sensor_34():
    data = request.json
    valor = data.get('valor')

    if valor is None:
        return jsonify({'error': 'No se envió el valor'}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sensor34 (valor) VALUES (%s)", (valor,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Dato guardado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50034)

import os
from llm_client import responder_llm
from db import init_db, guardar_postgres, leer_historial
from flask import Flask, request, jsonify

app = Flask(__name__)

# creamos la tabla feedback si aún no existe
init_db()

#------------ ELIMINAR PARA SUBIR A PRODUCCIÓN ------------#
app.config['DEBUG'] = True ### SÓLO PARA PRUEBAS 



#------------ HOME ------------#
@app.route("/", methods=["GET"])
def main():
    return "An LLM responding to users' feedback."



#------------ /FEEDBACK ------------#
@app.route("/feedback", methods=["POST"])
def feedback():
    # leemos el body de una solicitud http que ha llegado al servidor
    # si los datos son json los convierte en un diccionario de python (en 'data')
    # si no son json, devuelve None en lugar de lanzar una excepción 
    data = request.get_json(silent=True)

    # si la variable 'data' está vacía (porque no había datos o no eran json)
    # respondemos creamos un json con la respuesta de error 400 (bad request)
    # jsonify convierte en json un diccionario
    if not data:
        return jsonify({"Error": "No se han proporcionado datos en JSON."}), 400

    # intentamos leer la clave "texto" y si no existe se devuelve una clave vacía.
    # que guardamos en la variable 'texto'
    texto = data.get("texto", "").strip()

    # si el texto está vacío se devuelve un error 400
    if not texto:
        return jsonify({"error": "Campo 'texto' vacío"}), 400

    # Respuesta del LLM
    respuesta = responder_llm(texto) # llamada a la función en llm_client.py
    guardar_postgres(texto, respuesta) # guardamos feedback y respuesta en la base de datos postgres
    return jsonify({"respuesta": respuesta}), 200



#------------ /HISTORY ------------#
@app.route("/history", methods=["GET"])
def history():
    try:
        limite = int(request.args.get("n", 20))
    except ValueError:
        limite = 20
    registros = leer_historial(limite) # lista de diccionarios
    return jsonify(registros), 200



if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])

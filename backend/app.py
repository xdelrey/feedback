from flask import Flask, request, jsonify
import os

app = Flask(__name__)

########### ELIMINAR PARA SUBIR A PRODUCCIÓN #############
app.config['DEBUG'] = True ### SÓLO PARA PRUEBAS 

################## HOME ##################
@app.route("/", methods=["GET"])
def main():
    return "An LLM responding to users' feedback."

################## /FEEDBACK ##################
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

    # Respuesta provisional
    respuesta = f"Gracias por tu feedback: '{texto}'"
    return jsonify({"respuesta": respuesta}), 200

app.run()
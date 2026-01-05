# https://auth0.com/blog/developing-restful-apis-with-python-and-flask/
# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
from flask import Flask, jsonify, request
import json

with open('db.json', encoding='utf-8') as f:
    characters = json.load(f)
    print(characters)

app = Flask(__name__)


# Función auxiliar para procesar los datos según el idioma
def formatear_personajes(idioma):
    personajes_procesados = []

    for item in characters:
        # Creamos una copia del personaje para no modificar la base de datos original
        nuevo_personaje = item.copy()

        # Extraemos el objeto 'translations' y lo eliminamos del nuevo personaje
        # Si no existe 'translations', usamos un diccionario vacío
        traducciones = nuevo_personaje.pop('translations', {})

        # 2. SELECCIÓN DE IDIOMA:
        # Buscamos el idioma pedido. Si no existe, usamos 'es' por defecto (fallback)
        datos_texto = traducciones.get(idioma, traducciones.get('es', {}))

        # Mezclamos (merge) los datos de texto (nombre, desc) en el objeto principal
        nuevo_personaje.update(datos_texto)

        personajes_procesados.append(nuevo_personaje)

    return personajes_procesados


# RUTA DINÁMICA
# <lang> capturará "es" o "en" automáticamente
@app.route('/<lang>/characters')
def get_characters(lang):
    # Validamos que el idioma sea uno de los permitidos
    if lang not in ['es', 'en']:
        return jsonify({
            "error": "Idioma no soportado. Usa /es/characters o /en/characters",
            "rutas_disponibles": ["/es/characters", "/en/characters"]
        }), 400

    # Llamamos a nuestra función auxiliar
    resultado = formatear_personajes(lang)

    # Flask con jsonify ya se encarga de las cabeceras Content-Type: application/json
    # y de asegurar que la respuesta salga en UTF-8
    app.config['JSON_AS_ASCII'] = False  # Importante: permite tildes en la respuesta cruda
    return jsonify(resultado)


@app.route('/<lang>/characters/<int:id_character>')
def get_character_by_id(lang, id_character):
    # 1. Validar idioma
    if lang not in ['es', 'en']:
        return jsonify({"error": "Idioma no soportado"}), 400

    # 2. Buscar personaje en la base de datos (raw)
    # next() busca el primer elemento que coincida, o devuelve None
    personaje_encontrado = next((p for p in characters if p['id'] == id_character), None)

    if personaje_encontrado:
        # 3. Procesar idioma (misma lógica que arriba pero para uno solo)
        resultado = personaje_encontrado.copy()
        traducciones = resultado.pop('translations', {})
        datos_texto = traducciones.get(lang, traducciones.get('es', {}))
        resultado.update(datos_texto)

        app.config['JSON_AS_ASCII'] = False
        return jsonify(resultado)
    else:
        return jsonify({"error": "Personaje no encontrado"}), 404


# Ruta raíz para no dar error 404 si entran a la home
@app.route('/')
def home():
    return jsonify({
        "mensaje": "Bienvenido a la API de Personajes Retro",
        "rutas": {
            "personajes": "/es/characters",
            "por_id": "/en/characters/1"
        }
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
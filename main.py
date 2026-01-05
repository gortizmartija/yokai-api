from flask import Flask, jsonify
from data import get_db_json
from vars import TRANSLATIONS


yokais = get_db_json()

app = Flask(__name__)
app.json.sort_keys = False
app.json.ensure_ascii = False


def filter_yokais(lang):
    list_yokais = []

    for item in yokais:
        # Create a copy
        new_yokai = item.copy()

        translations = new_yokai.pop('translations', {})

        data_lang = translations.get(lang, translations.get('en', {}))

        # Update de yokai with the data of the lang
        new_yokai.update(data_lang)

        list_yokais.append(new_yokai)
    

    return list_yokais



@app.route('/<lang>/yokais')
def get_yokais(lang):
    # Validate the langs
    if lang not in TRANSLATIONS:
        return jsonify({
            "error": f"This lang is not supported: {lang}",
            "avaliable_langs": TRANSLATIONS
        }), 400

    result = filter_yokais(lang)

    app.config['JSON_AS_ASCII'] = False
    return jsonify(result)


@app.route('/<lang>/yokais/<int:id_yokai>')
def get_character_by_id(lang, id_yokai):
    if lang not in TRANSLATIONS:
        return jsonify({"error": f"This lang is not supported: {lang}"}), 400

    yokai_found = next((p for p in yokais if p['id'] == id_yokai), None)

    if yokai_found:
        result = yokai_found.copy()
        translations = result.pop('translations', {})
        data_lang = translations.get(lang, translations.get('en', {}))
        result.update(data_lang)

        app.config['JSON_AS_ASCII'] = False
        return jsonify(result)
    else:
        return jsonify({"error": "Yokai not found."}), 404


@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Yokais Public web API",
        "num_yokais" : len(yokais),
        "routes": {
            "yokais": "/en/yokais",
            "by_id": "/en/yokais/1"
        },
        "langs": TRANSLATIONS,
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
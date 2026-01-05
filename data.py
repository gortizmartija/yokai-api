# coding=utf-8

import pandas as pd
import json
import os

FILE = 'data.ods'
TRANSLATIONS = ['es', 'en']


def create_db_json():
    if not os.path.exists(FILE):
        print(f"❌ Error: Doesn't appear '{FILE}'")
        return

    print("📖 Reading File...")

    try:
        df_main = pd.read_excel(FILE, sheet_name='main').fillna('')

        dfs_translations = {}
        for lang in TRANSLATIONS:
            try:
                df_lang = pd.read_excel(FILE, sheet_name=lang).fillna('')
                df_lang.set_index('id', inplace=True)
                dfs_translations[lang] = df_lang
                print(f"   ✅ Tab '{lang}' loaded.")
            except ValueError:
                print(f"   ⚠️ Warning: No tab '{lang}' in the file.")

    except Exception as e:
        print(f"❌ Error crítico leyendo Excel: {e}")
        return

    json_output = []

    print("🔄 Procesando personajes...")
    for index, row in df_main.iterrows():
        personaje_id = row['id']

        personaje = {
            "id": int(personaje_id),
            "slug": row['slug'],
            "imagen": row['imagen'],
            "activo": bool(row['activo']),
            # Agrupamos las stats aquí mismo si están en la hoja main
            "stats": {
                "fuerza": int(row.get('fuerza', 0)),
                "velocidad": int(row.get('velocidad', 0)),
                "inteligencia": int(row.get('inteligencia', 0))
            },
            "translations": {}
        }

        # 4. Inyectamos los idiomas dinámicamente
        for lang, df_lang in dfs_idiomas.items():
            if personaje_id in df_lang.index:
                # Extraemos los datos de esa fila como diccionario
                datos_texto = df_lang.loc[personaje_id].to_dict()
                personaje['translations'][lang] = datos_texto
            else:
                # Si falta la traducción para este ID, ponemos un objeto vacío o un aviso
                print(f"   ⚠️ Falta traducción {lang} para ID {personaje_id}")
                personaje['translations'][lang] = {}

        json_output.append(personaje)

    # 5. Guardar JSON
    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump(json_output, f, indent=2, ensure_ascii=False)

    print(f"🎉 ¡Hecho! 'db.json' generado con {len(json_output)} personajes y {len(IDIOMAS_DISPONIBLES)} idiomas.")


if __name__ == '__main__':
    create_db_json()
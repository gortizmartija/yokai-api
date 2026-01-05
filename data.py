# coding=utf-8

import pandas as pd
from vars import FILE, TRANSLATIONS



def get_db_json():
    if not FILE.exists():
        print(f"❌ Error: Doesn't appear '{FILE}'")
        return []

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
        print(f"❌ Error reading the Excel: {e}")
        return []
    

    json_output = []

    print("🔄 Generating yokais...")
    for index, row in df_main.iterrows():
        yokai_id = row['id']

        yokai = {
            "id": int(yokai_id),
            "west_name": row['west_name'],
            "jp_name": row['jp_name'],
            "kanji_name": row['kanji_name'],
            "portrait_path": row['portrait_path'],
            "thumbnails_path": row['thumbnails_path'],
            "webp_path": row['webp_path'],
            "translations": {}
        }

        for lang, df_lang in dfs_translations.items():
            if yokai_id in df_lang.index:
                data_text = df_lang.loc[yokai_id].to_dict()
                yokai['translations'][lang] = data_text
            else:
                print(f"   ⚠️ Missing {lang} translation for the yokai with ID {yokai_id}")
                yokai['translations'][lang] = {}

        json_output.append(yokai)


    print(f"🎉 Done! data generated in json, {len(json_output)} yokais and {len(TRANSLATIONS)} langs.")
    return json_output



if __name__ == '__main__':
    get_db_json()
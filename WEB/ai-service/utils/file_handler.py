import json
import os

FILE_PATH = "data.json"


def read_json():
    """Membaca seluruh isi data.json"""
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(data):
    """Menimpa seluruh isi data.json"""
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def append_json(new_data):
    """Menambahkan data baru ke data.json"""
    data = read_json()
    data.append(new_data)
    write_json(data)
    return new_data
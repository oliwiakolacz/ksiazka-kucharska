import json
import os
from datetime import datetime


def get_default_filename():

    date_str = datetime.now().strftime("%Y%m%d")
    return f"przepisy_{date_str}.json"


def save_to_json(recipes, filename=None):

    if not recipes:
        print("\n[BLAD] Brak przepisow do zapisania.")
        return False
    
    if filename is None:
        default_name = get_default_filename()
        filename = input(f"Podaj nazwe pliku (domyslnie: {default_name}): ").strip()
        if not filename:
            filename = default_name
    
    # Dodanie rozszerzenia .json (jesli nie ma)
    if not filename.endswith('.json'):
        filename += '.json'
    
    try:
        # Wykorzystanie modulu json do zapisu
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(recipes, file, ensure_ascii=False, indent=2)
        
        # Wykorzystanie modulu os do sprawdzenia rozmiaru pliku
        file_size = os.path.getsize(filename)
        
        print(f"\n[OK] Zapisano {len(recipes)} przepis(ow) do pliku '{filename}'")
        print(f"[INFO] Rozmiar pliku: {file_size} bajtow")
        
        # Pokaz sciezke absolutna
        abs_path = os.path.abspath(filename)
        print(f"[INFO] Lokalizacja: {abs_path}")
        
        return True
        
    except IOError as e:
        print(f"\n[BLAD] Blad zapisu pliku: {e}")
        return False
    except Exception as e:
        print(f"\n[BLAD] Nieoczekiwany blad: {e}")
        return False


def load_from_json(filename=None):

    # Wyswietl dostepne pliki JSON w biezacym katalogu
    json_files = list_json_files()
    
    if json_files:
        print("\n[INFO] Dostepne pliki JSON w biezacym katalogu:")
        for i in range(len(json_files)):
            f = json_files[i]
            # Wyswietl rozmiar pliku
            size = os.path.getsize(f)
            print(f"   {i + 1}. {f} ({size} bajtow)")
    else:
        print("\n[INFO] Brak plikow JSON w biezacym katalogu.")
    
    if filename is None:
        filename = input("\nPodaj nazwe pliku do wczytania: ").strip()
    
    if not filename:
        print("[BLAD] Nie podano nazwy pliku.")
        return None
    
    # Dodanie rozszerzenia .json jesli nie ma
    if not filename.endswith('.json'):
        filename += '.json'
    
    # Sprawdzenie czy plik istnieje - modul os
    if not os.path.exists(filename):
        print(f"\n[BLAD] Plik '{filename}' nie istnieje.")
        return None
    
    try:
        # Wykorzystanie modulu json do odczytu
        with open(filename, 'r', encoding='utf-8') as file:
            recipes = json.load(file)
        
        # Walidacja struktury danych
        if not isinstance(recipes, list):
            print("\n[BLAD] Nieprawidlowy format pliku - oczekiwano listy przepisow.")
            return None
        
        # Walidacja kazdego przepisu
        valid_recipes = []
        for recipe in recipes:
            if validate_recipe_structure(recipe):
                valid_recipes.append(recipe)
            else:
                print(f"[UWAGA] Pominieto nieprawidlowy przepis: {recipe.get('name', 'bez nazwy')}")
        
        print(f"\n[OK] Wczytano {len(valid_recipes)} przepis(ow) z pliku '{filename}'")
        return valid_recipes
        
    except json.JSONDecodeError as e:
        print(f"\n[BLAD] Blad parsowania JSON: {e}")
        return None
    except IOError as e:
        print(f"\n[BLAD] Blad odczytu pliku: {e}")
        return None
    except Exception as e:
        print(f"\n[BLAD] Nieoczekiwany blad: {e}")
        return None


def validate_recipe_structure(recipe):

    required_fields = ['id', 'name', 'servings', 'ingredients', 'instructions']
    
    # Sprawdzenie wymaganych pol
    for field in required_fields:
        if field not in recipe:
            return False
    
    # Sprawdzenie typow
    if not isinstance(recipe['id'], int):
        return False
    if not isinstance(recipe['name'], str):
        return False
    if not isinstance(recipe['servings'], (int, float)):
        return False
    if not isinstance(recipe['ingredients'], list):
        return False
    if not isinstance(recipe['instructions'], str):
        return False
    
    # Sprawdzenie struktury skladnikow
    for ing in recipe['ingredients']:
        if not isinstance(ing, dict):
            return False
        if 'name' not in ing or 'amount' not in ing or 'unit' not in ing:
            return False
    
    return True


def list_json_files(directory="."):

    try:
        # Wykorzystanie os.listdir() i petli
        all_files = os.listdir(directory)
        json_files = []
        for f in all_files:
            if f.endswith('.json'):
                json_files.append(f)
        return sorted(json_files)
    except OSError:
        return []

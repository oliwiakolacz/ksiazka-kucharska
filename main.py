#!/usr/bin/env python3

# Import modulow wlasnych
from recipe_utils import (
    display_menu,
    clear_screen,
    get_valid_input,
    pause,
    confirm_action,
    format_recipe_full
)
from recipe_manager import RecipeManager
from file_handler import save_to_json, load_from_json

# Import modulow biblioteki standardowej
import sys


def show_welcome():

    print("""
    +---------------------------------------------------+
    |                                                   |
    |   WITAJ W KSIAZCE KUCHARSKIEJ!                    |
    |                                                   |
    |   Twoj osobisty asystent kulinarny                |
    |   Zarzadzaj swoimi przepisami  !                  |
    |                                                   |
    +---------------------------------------------------+
    """)


def main():

    # Inicjalizacja menedzera przepisow
    manager = RecipeManager()
    
    # Ekran powitalny
    show_welcome()
    
    # Dodanie przykladowych przepisow dla demonstracji
    add_sample_recipes(manager)
    
    # Glowna petla programu
    while True:
        display_menu()
        
        try:
            choice = input("Wybierz opcje (0-8): ").strip()
            
            if choice == "1":
                # Dodawanie nowego przepisu
                manager.add_recipe()
                pause()
                
            elif choice == "2":
                # Wyswietlanie wszystkich przepisow
                manager.list_all_recipes()
                
                # Opcja wyswietlenia
                if manager.get_all_recipes():
                    if confirm_action("\nCzy wyswietlic szczegoly konkretnego przepisu?"):
                        recipe_id = get_valid_input("Podaj ID przepisu: ", "int", min_val=1)
                        recipe = manager.get_recipe_by_id(recipe_id)
                        if recipe:
                            print(format_recipe_full(recipe))
                        else:
                            print(f"[BLAD] Nie znaleziono przepisu o ID {recipe_id}")
                pause()
                
            elif choice == "3":
                # Wyszukiwanie po nazwie
                manager.search_by_name()
                pause()
                
            elif choice == "4":
                # Wyszukiwanie po skladniku
                manager.search_by_ingredient()
                pause()
                
            elif choice == "5":
                # Edycja przepisu
                manager.edit_recipe()
                pause()
                
            elif choice == "6":
                # Usuwanie przepisu
                if confirm_action("Czy na pewno chcesz usunac przepis?"):
                    manager.delete_recipe()
                pause()
                
            elif choice == "7":
                # Zapis do pliku
                recipes = manager.get_all_recipes()
                save_to_json(recipes)
                pause()
                
            elif choice == "8":
                # Wczytanie z pliku
                loaded = load_from_json()
                if loaded:
                    if confirm_action("Czy zastapic obecne przepisy wczytanymi?"):
                        manager.set_recipes(loaded)
                        print("[OK] Przepisy zostaly wczytane.")
                    else:
                        # Dodaj do istniejacych
                        if confirm_action("Czy dodac wczytane przepisy do istniejacych?"):
                            current = manager.get_all_recipes()
                            # Aktualizacja ID dla nowych przepisow
                            max_id = 0
                            for r in current:
                                if r['id'] > max_id:
                                    max_id = r['id']
                            for recipe in loaded:
                                max_id += 1
                                recipe['id'] = max_id
                                current.append(recipe)
                            manager.set_recipes(current)
                            print("[OK] Przepisy zostaly dodane.")
                pause()
                
            elif choice == "0":
                # Wyjscie z programu
                print("\nDziekujemy za korzystanie z Ksiazki Kucharskiej!")
                print("Smacznego!\n")
                sys.exit(0)
                
            else:
                print("\n[BLAD] Nieprawidlowa opcja. Wybierz liczbe od 0 do 8.")
                
        except KeyboardInterrupt:
            print("\n\nProgram przerwany przez uzytkownika.")
            sys.exit(0)
        except Exception as e:
            print(f"\n[BLAD] Wystapil blad: {e}")
            pause()


def add_sample_recipes(manager):

    sample_recipes = [
        {
            "name": "Spaghetti Bolognese",
            "servings": 4,
            "ingredients": [
                {"name": "makaron spaghetti", "amount": 400, "unit": "g"},
                {"name": "mieso mielone wolowe", "amount": 500, "unit": "g"},
                {"name": "pomidory krojone", "amount": 400, "unit": "g"},
                {"name": "cebula", "amount": 1, "unit": "szt"},
                {"name": "czosnek", "amount": 3, "unit": "zabki"},
                {"name": "oliwa z oliwek", "amount": 2, "unit": "lyzki"}
            ],
            "instructions": "1. Podsmaz cebule i czosnek na oliwie. 2. Dodaj mieso i smaz do zrumienienia. 3. Dodaj pomidory i gotuj 20 min. 4. Ugotuj makaron al dente. 5. Podawaj sos na makaronie."
        },
        {
            "name": "Nalesniki",
            "servings": 6,
            "ingredients": [
                {"name": "maka pszenna", "amount": 250, "unit": "g"},
                {"name": "mleko", "amount": 500, "unit": "ml"},
                {"name": "jajka", "amount": 2, "unit": "szt"},
                {"name": "cukier", "amount": 2, "unit": "lyzki"},
                {"name": "maslo", "amount": 30, "unit": "g"},
                {"name": "sol", "amount": 1, "unit": "szczypta"}
            ],
            "instructions": "1. Wymieszaj make z jajkami. 2. Stopniowo dodawaj mleko, mieszajac. 3. Dodaj cukier i sol. 4. Smaz cienkie nalesniki na masle. 5. Podawaj z ulubionymi dodatkami."
        },
        {
            "name": "Salatka grecka",
            "servings": 2,
            "ingredients": [
                {"name": "pomidor", "amount": 2, "unit": "szt"},
                {"name": "ogorek", "amount": 1, "unit": "szt"},
                {"name": "ser feta", "amount": 150, "unit": "g"},
                {"name": "oliwki czarne", "amount": 50, "unit": "g"},
                {"name": "cebula czerwona", "amount": 0.5, "unit": "szt"},
                {"name": "oliwa z oliwek", "amount": 3, "unit": "lyzki"}
            ],
            "instructions": "1. Pokroj pomidory i ogorek w kostke. 2. Dodaj pokrojona cebule i oliwki. 3. Pokrusz fete na wierzch. 4. Polej oliwa i wymieszaj."
        }
    ]
    
    for recipe_data in sample_recipes:
        # Budowanie przepisu z odpowiednia struktura
        recipe = {
            "id": manager.next_id,
            "name": recipe_data["name"],
            "servings": recipe_data["servings"],
            "ingredients": recipe_data["ingredients"],
            "instructions": recipe_data["instructions"],
            "created_at": "2026-01-05"
        }
        manager.recipes.append(recipe)
        manager.next_id += 1
    
    print(f"[INFO] Zaladowano {len(sample_recipes)} przykladowych przepisow.")


if __name__ == "__main__":
    main()

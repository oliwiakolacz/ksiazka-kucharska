from datetime import datetime


def clear_screen():
    # Wyswietla pusta linie dla lepszej czytelnosci.
    print("\n" + "=" * 50 + "\n")


def display_menu():

    # Wyswietla glowne menu aplikacji.
    print("""
+--------------------------------------+
|       KSIAZKA KUCHARSKA              |
+--------------------------------------+
|  1. Dodaj nowy przepis               |
|  2. Wyswietl wszystkie przepisy      |
|  3. Wyszukaj przepis po nazwie       |
|  4. Wyszukaj po skladniku            |
|  5. Edytuj przepis                   |
|  6. Usun przepis                     |
|  7. Zapisz do pliku                  |
|  8. Wczytaj z pliku                  |
|  0. Wyjscie                          |
+--------------------------------------+
""")


def get_valid_input(prompt, input_type="str", min_val=None, max_val=None):

    # Pobiera i waliduje dane od uzytkownika.
    while True:
        user_input = input(prompt).strip()
        
        if input_type == "str":
            if user_input:
                return user_input
            print("[BLAD] Pole nie moze byc puste. Sprobuj ponownie.")
            
        elif input_type == "int":
            try:
                value = int(user_input)
                if min_val is not None and value < min_val:
                    print(f"[BLAD] Wartosc musi byc >= {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"[BLAD] Wartosc musi byc <= {max_val}")
                    continue
                return value
            except ValueError:
                print("[BLAD] Podaj liczbe calkowita.")
                
        elif input_type == "float":
            try:
                value = float(user_input)
                if min_val is not None and value < min_val:
                    print(f"[BLAD] Wartosc musi byc >= {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"[BLAD] Wartosc musi byc <= {max_val}")
                    continue
                return value
            except ValueError:
                print("[BLAD] Podaj liczbe.")


def format_recipe_short(recipe):

    # Formatuje przepis do krotkiego wyswietlenia (lista).
    ingredients_count = len(recipe.get("ingredients", []))
    return f"[{recipe['id']}] {recipe['name']} - {recipe['servings']} porcji, {ingredients_count} skladnikow"


def format_recipe_full(recipe):

    # Formatuje przepis do pelnego wyswietlenia.
    output = []
    output.append("\n" + "-" * 45)
    output.append(f"PRZEPIS: {recipe['name'].upper()}")
    output.append("-" * 45)
    output.append(f"ID: {recipe['id']}")
    output.append(f"Liczba porcji: {recipe['servings']}")
    output.append(f"Data dodania: {recipe.get('created_at', 'brak danych')}")
    
    output.append("\nSKLADNIKI:")
    for ing in recipe.get("ingredients", []):
        output.append(f"   - {ing['name']}: {ing['amount']} {ing['unit']}")
    
    output.append("\nINSTRUKCJE:")
    output.append(f"   {recipe.get('instructions', 'Brak instrukcji')}")
    output.append("-" * 45)
    
    return "\n".join(output)


def get_current_date():

    # Zwraca aktualna date w formacie YYYY-MM-DD.
    return datetime.now().strftime("%Y-%m-%d")


def confirm_action(message):

    # Prosi uzytkownika o potwierdzenie akcji.
    while True:
        response = input(f"{message} (t/n): ").strip().lower()
        if response in ['t', 'tak', 'y', 'yes']:
            return True
        elif response in ['n', 'nie', 'no']:
            return False
        print("[BLAD] Wpisz 't' (tak) lub 'n' (nie)")


def pause():

    # Zatrzymuje program do momentu nacisniecia Enter.
    input("\nNacisnij Enter, aby kontynuowac...")

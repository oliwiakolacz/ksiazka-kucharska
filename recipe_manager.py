from recipe_utils import get_valid_input, get_current_date, format_recipe_full, format_recipe_short


class RecipeManager:
    
    def __init__(self):

        # Inicjalizuje menedzer z pusta lista przepisow.
        self.recipes = []
        self.next_id = 1
    
    def add_recipe(self):

        # Dodaje nowy przepis na podstawie danych od uzytkownika.
        print("\nDODAWANIE NOWEGO PRZEPISU")
        print("-" * 35)
        
        # Pobieranie podstawowych danych
        name = get_valid_input("Nazwa przepisu: ", "str")
        servings = get_valid_input("Liczba porcji: ", "int", min_val=1)
        
        # Pobieranie skladnikow (lista slownikow)
        ingredients = []
        print("\nDodawanie skladnikow (wpisz 'koniec' aby zakonczyc):")
        
        while True:
            ing_name = input("  Nazwa skladnika (lub 'koniec'): ").strip()
            if ing_name.lower() == 'koniec':
                if not ingredients:
                    print("  [BLAD] Dodaj przynajmniej jeden skladnik!")
                    continue
                break
            
            if not ing_name:
                print("  [BLAD] Nazwa nie moze byc pusta.")
                continue
                
            amount = get_valid_input("  Ilosc: ", "float", min_val=0.01)
            unit = get_valid_input("  Jednostka (np. g, ml, szt, lyzka): ", "str")
            
            ingredients.append({
                "name": ing_name,
                "amount": amount,
                "unit": unit
            })
            print(f"  [OK] Dodano: {ing_name}")
        
        # Pobieranie instrukcji
        print("\nPodaj instrukcje przygotowania:")
        instructions = get_valid_input("Instrukcje: ", "str")
        
        # Tworzenie przepisu jako slownik
        recipe = {
            "id": self.next_id,
            "name": name,
            "servings": servings,
            "ingredients": ingredients,
            "instructions": instructions,
            "created_at": get_current_date()
        }
        
        # Dodanie do listy przepisow
        self.recipes.append(recipe)
        self.next_id += 1
        
        print(f"\n[OK] Przepis '{name}' zostal dodany pomyslnie!")
        return recipe
    
    def list_all_recipes(self):
        # Wyswietla wszystkie przepisy w skroconej formie.
        if not self.recipes:
            print("\n[INFO] Brak przepisow w ksiazce kucharskiej.")
            return
        
        print(f"\nWSZYSTKIE PRZEPISY ({len(self.recipes)}):")
        print("-" * 45)
        
        # Sortowanie po nazwie - wykorzystanie funkcji sorted() z key
        sorted_recipes = sorted(self.recipes, key=get_recipe_name_lower)
        
        for recipe in sorted_recipes:
            print(format_recipe_short(recipe))
    
    def search_by_name(self, search_term=None):
        # Wyszukuje przepisy po nazwie.
        if search_term is None:
            search_term = get_valid_input("\nPodaj nazwe do wyszukania: ", "str")
        
        search_term = search_term.lower()
        
        # Wyszukiwanie
        found = []
        for recipe in self.recipes:
            if search_term in recipe['name'].lower():
                found.append(recipe)
        
        if not found:
            print(f"\n[INFO] Nie znaleziono przepisow zawierajacych '{search_term}'")
        else:
            print(f"\n[OK] Znaleziono {len(found)} przepis(ow):")
            for recipe in found:
                print(format_recipe_full(recipe))
        
        return found
    
    def search_by_ingredient(self, ingredient=None):

        # Wyszukuje przepisy zawierajace okreslony skladnik.
        if ingredient is None:
            ingredient = get_valid_input("\nPodaj skladnik do wyszukania: ", "str")
        
        ingredient = ingredient.lower()
        found = []
        
        for recipe in self.recipes:
            # Sprawdzanie czy skladnik wystepuje w liscie skladnikow
            for ing in recipe['ingredients']:
                if ingredient in ing['name'].lower():
                    found.append(recipe)
                    break
        
        if not found:
            print(f"\n[INFO] Nie znaleziono przepisow ze skladnikiem '{ingredient}'")
        else:
            print(f"\n[OK] Znaleziono {len(found)} przepis(ow) ze skladnikiem '{ingredient}':")
            for recipe in found:
                print(format_recipe_short(recipe))
        
        return found
    
    def get_recipe_by_id(self, recipe_id):

        # Pobiera przepis po ID.
        for recipe in self.recipes:
            if recipe['id'] == recipe_id:
                return recipe
        return None
    
    def delete_recipe(self):

        # Usuwa przepis na podstawie ID.
        if not self.recipes:
            print("\n[INFO] Brak przepisow do usuniecia.")
            return False
        
        self.list_all_recipes()
        recipe_id = get_valid_input("\nPodaj ID przepisu do usuniecia: ", "int", min_val=1)
        
        recipe = self.get_recipe_by_id(recipe_id)
        
        if recipe is None:
            print(f"\n[BLAD] Nie znaleziono przepisu o ID {recipe_id}")
            return False
        
        # Usuniecie z listy
        self.recipes.remove(recipe)
        print(f"\n[OK] Przepis '{recipe['name']}' zostal usuniety.")
        return True
    
    def edit_recipe(self):

        # Edytuje istniejacy przepis.
        if not self.recipes:
            print("\n[INFO] Brak przepisow do edycji.")
            return None
        
        self.list_all_recipes()
        recipe_id = get_valid_input("\nPodaj ID przepisu do edycji: ", "int", min_val=1)
        
        recipe = self.get_recipe_by_id(recipe_id)
        
        if recipe is None:
            print(f"\n[BLAD] Nie znaleziono przepisu o ID {recipe_id}")
            return None
        
        print(format_recipe_full(recipe))
        print("\nCo chcesz zmienic?")
        print("1. Nazwe")
        print("2. Liczbe porcji")
        print("3. Instrukcje")
        print("4. Anuluj")
        
        choice = get_valid_input("Wybor: ", "int", min_val=1, max_val=4)
        
        if choice == 1:
            recipe['name'] = get_valid_input("Nowa nazwa: ", "str")
            print("[OK] Nazwa zostala zmieniona.")
        elif choice == 2:
            recipe['servings'] = get_valid_input("Nowa liczba porcji: ", "int", min_val=1)
            print("[OK] Liczba porcji zostala zmieniona.")
        elif choice == 3:
            recipe['instructions'] = get_valid_input("Nowe instrukcje: ", "str")
            print("[OK] Instrukcje zostaly zmienione.")
        else:
            print("Anulowano edycje.")
            return None
        
        return recipe
    
    def get_all_recipes(self):

        # Zwraca liste wszystkich przepisow.
        return self.recipes
    
    def set_recipes(self, recipes):

        # Ustawia liste przepisow (uzywane przy imporcie).
        self.recipes = recipes
        # Aktualizacja next_id na podstawie istniejacych przepisow
        if recipes:
            max_id = 0
            for r in recipes:
                if r['id'] > max_id:
                    max_id = r['id']
            self.next_id = max_id + 1
        else:
            self.next_id = 1


def get_recipe_name_lower(recipe):

    # Zwraca nazwe przepisu malymi literami.
    return recipe['name'].lower()

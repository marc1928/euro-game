import random
import os

def read_numbers_from_file(filename):
    """Lit les numéros stockés dans un fichier."""
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            numbers = [int(num) for line in lines for num in line.split()]
            return numbers
    except FileNotFoundError:
        print(f"Le fichier {filename} est introuvable.")
        return []
    except ValueError:
        print("Le fichier contient des données invalides.")
        return []

def generate_biased_numbers(available_numbers, count, max_value):
    """Génère des numéros en fonction de ceux disponibles dans le fichier."""
    if not available_numbers:
        print("Aucun numéro disponible, génération aléatoire complète.")
        return sorted(random.sample(range(1, max_value + 1), count))
    
    # Mélange des numéros stockés et génération aléatoire si nécessaire
    unique_numbers = list(set(available_numbers))  # Suppression des doublons
    generated = sorted(random.sample(unique_numbers, min(count, len(unique_numbers))))
    while len(generated) < count:
        remaining = random.randint(1, max_value)
        if remaining not in generated:
            generated.append(remaining)
    return sorted(generated)

def draw_numbers(main_file, stars_file):
    """Simule un tirage en utilisant les numéros des fichiers."""
    # Lecture des numéros principaux et des étoiles
    main_numbers_file = read_numbers_from_file(main_file)
    stars_numbers_file = read_numbers_from_file(stars_file)

    # Génération biaisée
    main_numbers = generate_biased_numbers(main_numbers_file, 5, 50)
    star_numbers = generate_biased_numbers(stars_numbers_file, 2, 12)

    return main_numbers, star_numbers

def main():
    print("Bienvenue dans la simulation EuroMillions avec des fichiers de numéros !")
    
    # Fichiers contenant les numéros et les étoiles (doivent être dans le même répertoire)
    main_file = os.path.join(os.getcwd(), "main_numbers.txt")
    stars_file = os.path.join(os.getcwd(), "stars.txt")
    
    # Nombre de tirages
    try:
        num_draws = int(input("Combien de tirages voulez-vous générer ? ").strip())
        if num_draws <= 0:
            print("Le nombre de tirages doit être supérieur à zéro.")
            return
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return

    # Générer les tirages
    for i in range(1, num_draws + 1):
        draw_main, draw_stars = draw_numbers(main_file, stars_file)
        print(f"Tirage {i} : Numéros principaux {draw_main}, Étoiles {draw_stars}")

if __name__ == "__main__":
    main()

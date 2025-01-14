import random
import os
from collections import Counter

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

def count_previous_draws_results(results_file):
    """Compte la fréquence des numéros dans les résultats précédents."""
    previous_results = read_numbers_from_file(results_file)
    return Counter(previous_results)

def filter_numbers_by_frequency(freq_counter, option):
    """Filtre les numéros selon leur fréquence d'apparition."""
    sorted_numbers = sorted(freq_counter.items(), key=lambda x: x[1])
    third = len(sorted_numbers) // 3

    if option == "moins sortis":
        return [num for num, _ in sorted_numbers[:third]]
    elif option == "plus sortis":
        return [num for num, _ in sorted_numbers[-third:]]
    elif option == "moyen":
        return [num for num, _ in sorted_numbers[third:-third]]
    elif option == "mixte":
        # Une combinaison équilibrée
        less_frequent = [num for num, _ in sorted_numbers[:third]]
        medium_frequent = [num for num, _ in sorted_numbers[third:-third]]
        most_frequent = [num for num, _ in sorted_numbers[-third:]]
        return less_frequent + medium_frequent + most_frequent
    else:
        print("Option invalide, tous les numéros seront considérés.")
        return list(freq_counter.keys())

def generate_biased_numbers(available_numbers, count, max_value):
    """Génère des numéros biaisés en fonction des résultats précédents (fréquence)."""
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

def draw_numbers(main_file, stars_file, results_file=None, bias_option=None):
    """Simule un tirage en utilisant les numéros des fichiers et en tenant compte des résultats précédents."""
    # Lecture des numéros principaux et des étoiles
    main_numbers_file = read_numbers_from_file(main_file)
    stars_numbers_file = read_numbers_from_file(stars_file)

    # Compter les anciens résultats si un fichier de résultats est fourni
    if results_file:
        freq_counter = count_previous_draws_results(results_file)
        main_numbers_file = filter_numbers_by_frequency(freq_counter, bias_option)

    # Génération biaisée
    main_numbers = generate_biased_numbers(main_numbers_file, 5, 50)
    star_numbers = generate_biased_numbers(stars_numbers_file, 2, 12)

    return main_numbers, star_numbers

def main():
    print("Bienvenue dans la simulation EuroMillions avec des fichiers de numéros !")
    
    # Fichiers contenant les numéros et les étoiles (doivent être dans le même répertoire)
    main_file = os.path.join(os.getcwd(), "main_numbers.txt")
    stars_file = os.path.join(os.getcwd(), "stars.txt")
    results_file = os.path.join(os.getcwd(), "previous_results.txt")  # Fichier des anciens résultats (optionnel)
    
    # Nombre de tirages
    try:
        num_draws = int(input("Combien de tirages voulez-vous générer ? ").strip())
        if num_draws <= 0:
            print("Le nombre de tirages doit être supérieur à zéro.")
            return
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return

    # Choisir le type de biais
    print("Choisissez l'analyse des numéros (options : 'moins sortis', 'plus sortis', 'moyen', 'mixte') :")
    bias_option = input("Votre choix : ").strip().lower()
    
    # Générer les tirages
    for i in range(1, num_draws + 1):
        draw_main, draw_stars = draw_numbers(main_file, stars_file, results_file, bias_option)
        print(f"Tirage {i} : Numéros principaux {draw_main}, Étoiles {draw_stars}")

if __name__ == "__main__":
    main()

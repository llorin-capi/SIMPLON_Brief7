import requests
import random

# Listing des IDs possibles
id_possibles = list(range(1, 1026)) + list(range(10001, 10278))

# Fonction pour récupérer les données d'un Pokémon
def donnees_pokemon(url):
    response = requests.get(url)
    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_name = pokemon_data["name"]
        pokemon_hp = pokemon_data["stats"][0]['base_stat']
        pokemon_attack = pokemon_data["stats"][1]['base_stat']
        pokemon_defense = pokemon_data["stats"][2]['base_stat']
        pokemon_special_attack = pokemon_data["stats"][3]['base_stat']
        pokemon_special_defense = pokemon_data["stats"][4]['base_stat']
        pokemon_speed = pokemon_data["stats"][5]['base_stat']
        
        return {
            'name': pokemon_name,
            'hp': pokemon_hp,
            'attack': pokemon_attack,
            'defense': pokemon_defense,
            'special_attack': pokemon_special_attack,
            'special_defense': pokemon_special_defense,
            'speed': pokemon_speed
        }
    else:
        return None


# Fonction pour sélectionner un Pokémon aléatoire parmi les IDs disponibles
def pokemon_aleatoire():
    nombre_aleatoire = random.choice(id_possibles)
    url_pokemon_aleatoire = f'https://pokeapi.co/api/v2/pokemon/{nombre_aleatoire}'
    return donnees_pokemon(url_pokemon_aleatoire)

# Calcul de l'attaque totale et de la défense totale
def calculer_stats_totales(pokemon):
    total_attack = (pokemon['attack'] + pokemon['special_attack']) / 2 # moyenne ATT et ATT SPE
    total_defense = (pokemon['defense'] + pokemon['special_defense']) / 2 # moyenne DEF et DEF SPE
    return total_attack, total_defense

# Simuler un combat entre deux Pokémons
def simuler_combat(pokemon1, pokemon2):
    attack_pokemon1, defense_pokemon1 = calculer_stats_totales(pokemon1)
    attack_pokemon2, defense_pokemon2 = calculer_stats_totales(pokemon2)

    # Dégâts infligés par chaque Pokémon
    degats_pokemon1 = max(0, attack_pokemon1 - defense_pokemon2)
    degats_pokemon2 = max(0, attack_pokemon2 - defense_pokemon1)

    # Réduction des HP des Pokémons
    pokemon1['hp'] -= degats_pokemon2
    pokemon2['hp'] -= degats_pokemon1

    # Déterminer le gagnant
    if pokemon1['hp'] > pokemon2['hp']:
        return pokemon1
    elif pokemon2['hp'] > pokemon1['hp']:
        return pokemon2
    else:
        return random.choice([pokemon1, pokemon2])  # En cas d'égalité, le gagnant est choisi aléatoirement

# Fonction pour simuler un tournoi
def tournoi_pokemon():
    # Sélectionner 16 Pokémon aléatoires pour le tournoi
    participants = [pokemon_aleatoire() for _ in range(16)]
    # Affichage des 16 Pokémons sélectionnés
    print
    print("Participants du tournoi :")
    for participant in participants:
        print(participant['name'].upper())        
        # Afficher la moyenne d'attaque et de défense avec f-strings
        print(f"attack : {(participant['attack'] + participant['special_attack']) / 2}")
        print(f"defense : {(participant['defense'] + participant['special_defense']) / 2}")

    # Simuler les tours du tournoi
    round_number = 1
    while len(participants) > 1:
        print(f"\n--- Tour {round_number} ---")
        round_number += 1
        prochains_tours = []
        
        # Simuler chaque duel
        for i in range(0, len(participants), 2):
            pokemon1 = participants[i]
            pokemon2 = participants[i + 1]
            gagnant = simuler_combat(pokemon1, pokemon2)
            print(f"{pokemon1['name'].capitalize()} contre {pokemon2['name'].capitalize()} --> {gagnant['name'].capitalize()} gagne !")
            prochains_tours.append(gagnant)
        
        # Les gagnants passent au tour suivant
        participants = prochains_tours

    # Déclarer le vainqueur
    print(f"\nLe grand gagnant du tournoi est {participants[0]['name'].capitalize()} !")

# Démarrer le tournoi
tournoi_pokemon()

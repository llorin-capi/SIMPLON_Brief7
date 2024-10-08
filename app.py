from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# Liste des IDs possibles pour les Pokémon
id_possibles = list(range(1, 1026))

# Fonction pour récupérer les données d'un Pokémon
def donnees_pokemon():
    nombre_aleatoire = random.choice(id_possibles)
    url_pokemon_aleatoire = f'https://pokeapi.co/api/v2/pokemon/{nombre_aleatoire}'
    response = requests.get(url_pokemon_aleatoire)
    if response.status_code == 200:
        pokemon_data = response.json()
        return {
            'name': pokemon_data["name"].capitalize(),
            'hp': pokemon_data["stats"][0]['base_stat'],
            'attack': pokemon_data["stats"][1]['base_stat'],
            'defense': pokemon_data["stats"][2]['base_stat'],
            'special_attack': pokemon_data["stats"][3]['base_stat'],
            'special_defense': pokemon_data["stats"][4]['base_stat'],
            'speed': pokemon_data["stats"][5]['base_stat'],
            'sprite': pokemon_data['sprites']['front_default']
        }
    else:
        return None
@app.route('/')

def index():
    # Par défaut 16 participants, sinon récupère le nombre depuis les paramètres de la requête
    nombre_participants = int(request.args.get('participants', 16))
    participants = [donnees_pokemon() for _ in range(nombre_participants)]

    rounds = []
    round_number = 1
    while len(participants) > 1:
        round_info = []
        for i in range(0, len(participants), 2):
            # Vérification pour éviter des erreurs lorsque le nombre de participants est impair
            if i + 1 < len(participants):
                pokemon1 = participants[i]
                pokemon2 = participants[i + 1]
                gagnant, battle_log = simuler_combat(pokemon1, pokemon2)
                round_info.append({
                    'pokemon1': pokemon1,
                    'pokemon2': pokemon2,
                    'winner': gagnant,
                    'log': battle_log  # Ajouter le log du combat
                })
        participants = [match['winner'] for match in round_info]
        rounds.append({
            'round_number': round_number,
            'matches': round_info
        })
        round_number += 1

    winner = participants[0]

    return render_template('lea_front.html', rounds=rounds, winner=winner, nombre_participants=nombre_participants)

def calculer_degats(attaque, defense):
    # Formule pour calculer des dégâts plus réalistes
    multiplicateur = random.uniform(0.85, 1.0)  # Facteur aléatoire entre 0.85 et 1.0
    degats = ((attaque * 2) / (defense + 1)) * multiplicateur
    return max(1, round(degats))  # Toujours au moins 1 dégât

# On détermine qui commence (comparaison vitesse)
def ordre_tour(pokemon1,pokemon2, speed_pokemon1, speed_pokemon2) :
    if speed_pokemon1>speed_pokemon2 : 
        commence=pokemon1
        termine=pokemon2
    else :
        if speed_pokemon1== speed_pokemon2 :
            n=random.choice([0,1])
            if n==1 :
                commence=pokemon1
                termine=pokemon2
            else :
                commence=pokemon2
                termine=pokemon1
        else : 
            commence=pokemon2
            termine=pokemon1
    return commence, termine

def calculer_stats_totales(pokemon):
    """
    Calcule les statistiques d'attaque et de défense moyennes d'un Pokémon
    (attaque + attaque spéciale) / 2 et (défense + défense spéciale) / 2.
    """
    total_attack = (pokemon['attack'] + pokemon['special_attack']) / 2
    total_defense = (pokemon['defense'] + pokemon['special_defense']) / 2
    return total_attack, total_defense

# Simulation d'un combat
def simuler_combat(pokemon1, pokemon2):
    speed_pokemon1 = pokemon1['speed']
    speed_pokemon2 = pokemon2['speed']

    pokemon_commence, pokemon_termine = ordre_tour(pokemon1, pokemon2, speed_pokemon1, speed_pokemon2)

    # Calcul des statistiques totales d'attaque et de défense
    attaque_pokemon_commence = (pokemon_commence['attack'] + pokemon_commence['special_attack']) / 2
    defense_pokemon_commence = (pokemon_commence['defense'] + pokemon_commence['special_defense']) / 2

    attaque_pokemon_termine = (pokemon_termine['attack'] + pokemon_termine['special_attack']) / 2
    defense_pokemon_termine = (pokemon_termine['defense'] + pokemon_termine['special_defense']) / 2

    hp_commence = pokemon_commence['hp']
    hp_termine = pokemon_termine['hp']

    defense_restante_pokemon_commence = defense_pokemon_commence
    defense_restante_pokemon_termine = defense_pokemon_termine

    # Créer une liste pour stocker chaque tour de combat
    battle_log = []

    while hp_commence > 0 and hp_termine > 0 :
        # Attaque du Pokémon qui commence le tour
        if attaque_pokemon_commence >= defense_restante_pokemon_termine:
            degats_aux_hp = attaque_pokemon_commence - defense_restante_pokemon_termine
            hp_termine = max(0, hp_termine - degats_aux_hp)
            defense_restante_pokemon_termine = 0
        else:
            defense_restante_pokemon_termine -= attaque_pokemon_commence

        # On ajoute le log de l'attaque à la liste
        battle_log.append({
            'attacker': pokemon_commence['name'],
            'defender': pokemon_termine['name'],
            'degats': attaque_pokemon_commence,
            'hp_initial': pokemon_termine['hp'],
            'hp_restants': hp_termine,
            'defense_initial': defense_pokemon_termine,
            'defense_restante': defense_restante_pokemon_termine
        })

        # On contrôle si l'adversaire a encore des PVs, sinon on arrête le combat
        if hp_termine <= 0:
            battle_log.append({
                'message': f"{pokemon_termine['name']} est KO. Vainqueur : {pokemon_commence['name']}",
                'ko': True  # Marquer Pokémon 2 KO
            })
            break 

        # Attaque du Pokémon qui termine le tour
        if attaque_pokemon_termine >= defense_restante_pokemon_commence:
            degats_aux_hp = attaque_pokemon_termine - defense_restante_pokemon_commence
            hp_commence = max(0, hp_commence - degats_aux_hp)
            defense_restante_pokemon_commence = 0
        else:
            defense_restante_pokemon_commence -= attaque_pokemon_termine

        # Ajouter les informations de cette attaque à la liste
        battle_log.append({
            'attacker': pokemon_termine['name'],
            'defender': pokemon_commence['name'],
            'degats': attaque_pokemon_termine,
            'hp_initial': pokemon_commence['hp'],
            'hp_restants': hp_commence,
            'defense_initial': defense_pokemon_commence,
            'defense_restante': defense_restante_pokemon_commence
        })

        # On contrôle si le premier Pokémon a encore des PVs
        if hp_commence <= 0:
            battle_log.append({
                'message': f"{pokemon_commence['name']} est KO. Vainqueur : {pokemon_termine['name']}",
                'ko': True  # Marquer Pokémon 1 KO
            })
            break


    # On retourne le vaiqueur
    if hp_commence > 0:
        return pokemon_commence, battle_log
    elif hp_termine > 0:
        return pokemon_termine, battle_log
    else :
        return random.choice([pokemon_commence, pokemon_termine]), battle_log

if __name__ == '__main__':
    app.run()
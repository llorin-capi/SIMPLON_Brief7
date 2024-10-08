from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# Liste des IDs possibles pour les Pokémon
id_possibles = list(range(1, 1026)) + list(range(10001, 10278))

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


def calculer_stats_totales(pokemon):
    """
    Calcule les statistiques d'attaque et de défense moyennes d'un Pokémon
    (attaque + attaque spéciale) / 2 et (défense + défense spéciale) / 2.
    """
    total_attack = (pokemon['attack'] + pokemon['special_attack']) / 2
    total_defense = (pokemon['defense'] + pokemon['special_defense']) / 2
    return total_attack, total_defense

def simuler_combat(pokemon1, pokemon2):
    """
    Simule un combat entre deux Pokémon en utilisant la formule de combat demandée.
    La défense se réduit avant d'affecter les HP. Si la défense est épuisée, les dégâts affectent les HP.
    """
    # Calcul des statistiques totales d'attaque et de défense
    total_attack_pokemon1 = (pokemon1['attack'] + pokemon1['special_attack']) / 2
    total_defense_pokemon1 = (pokemon1['defense'] + pokemon1['special_defense']) / 2

    total_attack_pokemon2 = (pokemon2['attack'] + pokemon2['special_attack']) / 2
    total_defense_pokemon2 = (pokemon2['defense'] + pokemon2['special_defense']) / 2

    # Stocker les HP et défenses initiaux
    hp_initial_pokemon1 = pokemon1['hp']
    hp_initial_pokemon2 = pokemon2['hp']

    defense_restante_pokemon1 = total_defense_pokemon1
    defense_restante_pokemon2 = total_defense_pokemon2

    # Créer une liste pour stocker chaque tour de combat
    battle_log = []

    # Tant que les deux Pokémon ont encore des HP positifs
    while pokemon1['hp'] > 0 and pokemon2['hp'] > 0:
        # Attaque de Pokémon 1 sur Pokémon 2
        if total_attack_pokemon1 >= defense_restante_pokemon2:
            degats_aux_hp = total_attack_pokemon1 - defense_restante_pokemon2
            pokemon2['hp'] = max(0, pokemon2['hp'] - degats_aux_hp)
            defense_restante_pokemon2 = 0
        else:
            defense_restante_pokemon2 -= total_attack_pokemon1

        # Ajouter les informations de cette attaque à la liste
        battle_log.append({
            'attacker': pokemon1['name'],
            'defender': pokemon2['name'],
            'degats': total_attack_pokemon1,
            'hp_initial': hp_initial_pokemon2,
            'hp_restants': pokemon2['hp'],
            'defense_initial': total_defense_pokemon2,
            'defense_restante': defense_restante_pokemon2
        })

        # Vérifier si Pokémon 2 est KO
        if pokemon2['hp'] <= 0:
            battle_log.append({
                'message': f"{pokemon2['name']} est KO. Vainqueur : {pokemon1['name']}",
                'ko': True  # Marquer Pokémon 2 KO
            })
            return pokemon1, battle_log  # Pokémon 1 gagne si Pokémon 2 est KO

        # Attaque de Pokémon 2 sur Pokémon 1
        if total_attack_pokemon2 >= defense_restante_pokemon1:
            degats_aux_hp = total_attack_pokemon2 - defense_restante_pokemon1
            pokemon1['hp'] = max(0, pokemon1['hp'] - degats_aux_hp)
            defense_restante_pokemon1 = 0
        else:
            defense_restante_pokemon1 -= total_attack_pokemon2

        # Ajouter les informations de cette attaque à la liste
        battle_log.append({
            'attacker': pokemon2['name'],
            'defender': pokemon1['name'],
            'degats': total_attack_pokemon2,
            'hp_initial': hp_initial_pokemon1,
            'hp_restants': pokemon1['hp'],
            'defense_initial': total_defense_pokemon1,
            'defense_restante': defense_restante_pokemon1
        })

        # Vérifier si Pokémon 1 est KO
        if pokemon1['hp'] <= 0:
            battle_log.append({
                'message': f"{pokemon1['name']} est KO. Vainqueur : {pokemon2['name']}",
                'ko': True  # Marquer Pokémon 1 KO
            })
            return pokemon2, battle_log  # Pokémon 2 gagne si Pokémon 1 est KO

    return random.choice([pokemon1, pokemon2]), battle_log

if __name__ == '__main__':
    app.run(debug=True)

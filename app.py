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
    # Par défaut 8 participants, sinon récupère le nombre depuis les paramètres de la requête
    nombre_participants = int(request.args.get('participants', 8))
    participants = [donnees_pokemon() for _ in range(nombre_participants)]

    rounds = []
    round_number = 1
    while len(participants) > 1:
        round_info = []
        for i in range(0, len(participants), 2):
            pokemon1 = participants[i]
            pokemon2 = participants[i + 1]
            gagnant = simuler_combat(pokemon1, pokemon2)
            round_info.append({
                'pokemon1': pokemon1,
                'pokemon2': pokemon2,
                'winner': gagnant
            })
        participants = [match['winner'] for match in round_info]
        rounds.append({
            'round_number': round_number,
            'matches': round_info
        })
        round_number += 1

    winner = participants[0]

    return render_template('lea_front.html', rounds=rounds, winner=winner)


def calculer_stats_totales(pokemon):
    total_attack = (pokemon['attack'] + pokemon['special_attack']) / 2
    total_defense = (pokemon['defense'] + pokemon['special_defense']) / 2
    return total_attack, total_defense

def simuler_combat(pokemon1, pokemon2):
    attack_pokemon1, defense_pokemon1 = calculer_stats_totales(pokemon1)
    attack_pokemon2, defense_pokemon2 = calculer_stats_totales(pokemon2)

    degats_pokemon1 = max(0, attack_pokemon1 - defense_pokemon2)
    degats_pokemon2 = max(0, attack_pokemon2 - defense_pokemon1)

    pokemon1['hp'] -= degats_pokemon2
    pokemon2['hp'] -= degats_pokemon1

    if pokemon1['hp'] > pokemon2['hp']:
        return pokemon1
    elif pokemon2['hp'] > pokemon1['hp']:
        return pokemon2
    else:
        return random.choice([pokemon1, pokemon2])

if __name__ == '__main__':
    app.run(debug=True)
import json
import requests
import collections

Player = collections.namedtuple('Player',
                                ['account_id', 'best_hero', 'kda', 'gold_per_min', 'xp_per_min', 'last_hits', 'denies',
                                 'lane_efficiency_pct', 'hero_damage', 'tower_damage', 'hero_healing',
                                 'stuns', 'tower_kills', 'neutral_kills', 'courier_kills', 'actions_per_min'])


def call_opendota(path, query=None):
    url = 'https://api.opendota.com/api/' + '/'.join(map(str, path))
    if query is not None:
        url += '?' + '&'.join([k + '=' + str(v) for k, v in query.items()])
    print(url)
    res = requests.get(url)
    data = json.loads(res.content.decode('utf-8'))
    return data


def resolve(player):
    if type(player) == int:
        return player

    if player.isdigit():
        return player
    else:
        data = call_opendota(('search', ''), {'q': player, 'similarity': 1})
        # TODO: catch when there are no players returned
        return data[0]['account_id']


HEROES = None
players_data_local = None


def heroes():
    global HEROES
    if HEROES is not None:
        return HEROES
    data = call_opendota(('heroes',))
    HEROES = {str(hero['id']): hero['localized_name'] for hero in data}
    print('preloaded heroes')
    return HEROES


def get_stats(player, players_data_locally=None):
    player = resolve(player)
    print("Getting status of player: " + str(player))
    data = fetch_stats(players_data_locally, player)
    # want kda, gpm, xpm [3:6]
    players_stats = dict(map(lambda stat: (stat['field'], stat['sum'] / stat['n'] if stat['n'] > 0 else 0), data))
    return Player(
        account_id=player,
        best_hero=get_best_hero(player, players_data_locally),
        kda=float(players_stats['kda']),
        gold_per_min=float(players_stats['gold_per_min']),
        xp_per_min=float(players_stats['xp_per_min']),
        last_hits=float(players_stats['last_hits']),
        denies=float(players_stats['denies']),
        lane_efficiency_pct=float(players_stats['lane_efficiency_pct']),
        hero_damage=float(players_stats['hero_damage']),
        tower_damage=float(players_stats['tower_damage']),
        hero_healing=float(players_stats['hero_healing']),
        stuns=float(players_stats['stuns']),
        tower_kills=float(players_stats['tower_kills']),
        neutral_kills=float(players_stats['neutral_kills']),
        courier_kills=float(players_stats['courier_kills']),
        actions_per_min=float(players_stats['actions_per_min'])
    )


def fetch_stats(players_data_locally, player):
    if players_data_locally is None:
        return call_opendota(('players', player, 'totals'))
    else:
        return json.loads(players_data_locally[str(player)].split('$$__$$')[0])


def get_best_hero(player, players_data_locally):

    if players_data_locally is None:
        data = call_opendota(('players', player, 'heroes'))
        best_hero = max(data, key=lambda h: h['win'] / h['games'] if h['games'] > 0 else 0)
        return int(best_hero['hero_id'])
    else:
        return int(players_data_locally[str(player)].split('$$__$$')[1])

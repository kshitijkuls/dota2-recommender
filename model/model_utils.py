from constants import model_constants
from joblib import Parallel, delayed

from api import opendota


def get_player_df(spark, training_size, mode):
    pro_players = opendota.call_opendota(('proplayers', ''))
    import itertools
    players_account = itertools.islice({player['account_id'] for player in pro_players}, int(training_size))
    return prepare_player_df(players_account, spark, mode)


def prepare_player_df(players_account, spark, mode=model_constants.LOCAL_MODE):
    players_data = fetch_players_data_locally(mode)
    players_stats = Parallel(n_jobs=12, backend="threading")(
        delayed(opendota.get_stats)(player, players_data) for player in players_account)

    data_df = spark.createDataFrame(players_stats)
    return data_df


def fetch_players_data_locally(mode):
    if mode == model_constants.LOCAL_MODE:
        return players_data_locally()


def players_data_locally():
    file = open("data/local_data.txt", "r")
    players_data_local = dict(map(lambda player_info: (player_info.split('#')), file.read().split('\n')))
    return players_data_local

if __name__ == '__main__':
    players_data_locally()
from api import opendota
from constants import model_constants
from model import model_fitter
from flask import Flask, request
from flask import render_template
from flask.json import jsonify
from model import predictor

app = Flask(__name__)


# @api.route('/leaderboard')
@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    player_ids = request.args.get("player_ids").split(',')
    print(player_ids)
    time_frame = request.args.get("time_window")
    board = []
    players = [opendota.resolve(player_id) for player_id in player_ids]
    days = model_constants.TIME_WINDOW[time_frame]
    print(players)
    for player in players:
        data = opendota.call_opendota(('players', player, 'wl'), {'date': days})
        wins = data['win']
        board.append({'account_id': player, 'wins': wins, 'win_rate': wins / days})
    print(board)
    return jsonify(sorted(board, key=lambda x: -x['win_rate']))


@app.route('/compare', methods=['GET'])
def compare():
    player1 = opendota.get_stats(request.args.get("player1"))
    player2 = opendota.get_stats(request.args.get("player2"))
    result = {}
    # for A_stat, B_stat in zip(player1, player2):
    #     if A_stat[1] > B_stat[1]:
    #         result[A_stat[0]] = A_stat[1]
    #     else:
    #         result[A_stat[0]] = B_stat[1]

    labels = ['kda', 'last_hits/10', 'actions_per_min/10', 'neutral_kills/10', 'tower_kills', 'tower_damage/100',
              'hero_damage/1000', 'gold_per_min/1000', 'xp_per_min/100']
    values = [
        (player1.kda, player2.kda),
        (player1.last_hits/10, player2.last_hits/10),
        (player1.actions_per_min/10, player2.actions_per_min/10),
        (player1.neutral_kills/10, player2.neutral_kills/10),
        (player1.tower_kills, player2.tower_kills),
        (player1.tower_damage/100, player2.tower_damage/100),
        (player1.hero_damage/1000, player2.hero_damage/1000),
        (player1.gold_per_min/100, player2.gold_per_min/100),
        (player1.xp_per_min/100, player2.xp_per_min/100)
    ]

    return render_template('chart.html', values=values, labels=labels)


@app.route('/suggest', methods=['GET'])
def suggest():
    player = opendota.resolve(request.args.get("player"))
    result = {'suggested_hero': predictor.predict(player)}
    return jsonify(result)


# Train model
@app.route('/train', methods=['GET'])
def train_model():
    model_fitter.train_model(request.args.get("training_size", default=model_constants.TRAINING_SIZE),
                             model_constants.REMOTE_MODE)
    result = {'message': 'Training done', 'status': '200'}
    return jsonify(result)


@app.route('/train_locally', methods=['GET'])
def train_model_locally():
    model_fitter.train_model(request.args.get("training_size", default=model_constants.TRAINING_SIZE),
                             model_constants.LOCAL_MODE)
    result = {'message': 'Training done', 'status': '200'}
    return jsonify(result)


@app.route("/")
def chart():
    return render_template('main.html', values=None, labels=None)


if __name__ == '__main__':
    app.run(debug=True)  # Start a development server

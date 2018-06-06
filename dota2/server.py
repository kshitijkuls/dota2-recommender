from flask import Flask, request
from flask.json import jsonify
from dota2.api import opendota
from dota2.model import predictor
from dota2.model import model_fitter
from dota2.constants import model_constants

app = Flask(__name__)  # Create a Flask WSGI application


# Question 1
# @api.route('/leaderboard')
@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    player_ids = request.args.get("player_ids").split(',')
    print(player_ids)
    time_frame = request.args.get("time_frame")
    board = []
    # handle if personaname is given instead of account_id
    players = [opendota.resolve(player_id) for player_id in player_ids]
    days = opendota.INTERVALS[time_frame]
    # now = datetime.now()
    print(players)
    for player in players:
        data = opendota.call_opendota(('players', player, 'wl'), {'date': days})
        wins = data['win']
        board.append({'account_id': player, 'wins': wins, 'win_rate': wins / days})
    print(board)
    return jsonify(sorted(board, key=lambda x: -x['win_rate']))


# Question 2
@app.route('/compare', methods=['GET'])
def compare():
    player1 = opendota.get_stats(request.args.get("player1"))
    player2 = opendota.get_stats(request.args.get("player2"))
    result = {}
    for A_stat, B_stat in zip(player1, player2):
        if A_stat[1] > B_stat[1]:
            result[A_stat[0]] = A_stat[1]
        else:
            result[A_stat[0]] = B_stat[1]
    return jsonify(result)


# Question 3
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


if __name__ == '__main__':
    app.run(debug=True)  # Start a development server

    # if __name__ == '__main__':
    #     print(opendota.players_data_locally()['163870721'])

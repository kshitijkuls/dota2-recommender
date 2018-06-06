# dota2 API

###1. Leaderboard

1.1 `GET /leaderboard?player_ids={account_ids}&time_window={time_window}`

1.2 `GET /leaderboard?player_ids={usernames}&time_window={time_window}`

       e.g`/leaderboard?player_ids=108383863,142589406&time_window=year`

* player_ids - a comma separated list of `account_id` / `username`
* time_window - accepted values => `week` / `month` / `year`

###2. Players Comparison

`GET /compare?player1={account_id}&player2={account_id}`
* player1 - `account_id` / `player_name`
* player2 - `account_id` / `player_name`

      e.g`/compare?player1=87776861&player2=112127585`

###3. Recommendation Engine (Recommend hero)

`GET /suggest?player={account_id}`
* player - `account_id` / `player_name`

      e.g`/suggest?player=108383863`

####3.1 Train model (remote-data)
`GET /train?training_size={training_size}`

######Note: Training size is optional, `default = 2000`

####3.2 Train model (local-data)
`GET /train_locally?training_size={training_size}`

######Note: Training size is optional, `default = 2000`

####3.3 Suggest hero to a player
`GET /suggest?player={account_id}`

##Setup

1. `pip3 install -r requirements.txt`

2. `python3 server.py`
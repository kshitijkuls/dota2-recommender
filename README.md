# dota2 API

###1. Leaderboard

1.1 `GET /leaderboard?player_ids={account_ids}&time_window={time_window}`

1.2 `GET /leaderboard?player_ids={usernames}&time_window={time_window}`

       e.g`/leaderboard?player_ids=76482434,zAHARASAURUS&time_window=month`

* player_ids - a comma separated list of `account_id` / `username`
* time_window - accepted values => `week` / `month` / `year`

    ```javascript
    Sample Response
    [{
    "account_id": 76482434,
    "win_rate": 2.033333333333333,
    "wins": 61
  },
  {
    "account_id": 88018,
    "win_rate": 0.8333333333333334,
    "wins": 25
  }]```

###2. Players Comparison

`GET /compare?player1={account_id}&player2={account_id}`
* player1 - `account_id` / `player_name`
* player2 - `account_id` / `player_name`

      e.g /compare?player1=87776861&player2=112127585

`Sample response`
<img src="https://github.com/horizon23/dota2-recommonder/blob/master/comparison.png" height="540" width="780">

###3. Recommendation Engine (Recommend hero)

`GET /suggest?player={account_id}`
* player - `account_id` / `player_name`

      e.g /suggest?player=108383863

####3.1 Train model (remote-data)
`GET /train?training_size={training_size}`

######Note: Training size is optional, `default = 2000`

####3.2 Train model (local-data)
`GET /train_locally?training_size={training_size}`

######Note: Training size is optional, `default = 2000`

####3.3 Suggest hero to a player
`GET /suggest?player={account_id}`


```javascript
Sample Response
{
  "suggested_hero": "Brewmaster"
}
```
##Setup

1. `pip3 install -r requirements.txt`

2. `python3 server.py`

Server link: `http://localhost:5000/`
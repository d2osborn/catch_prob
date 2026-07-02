"""
finds the venue id and venue name for each game, creates a json file to access the venue_ids by gamepk
"""
import pandas as pd
import requests
import json

def venue_identifier(gamePk):
    """
    api request to mlb stats api schedule endpoint to find what the venue was for a given gamepk
    """
    url = 'https://statsapi.mlb.com/api/v1/schedule'
    params = {'sportId': '1', 
              'gamePk': f"{gamePk}"
              }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            game_data = data['dates'][0]['games'][0]
            venue_id = game_data['venue']['id']
            venue_name = game_data['venue']['name']

            return [venue_id, venue_name]
    except (KeyError, IndexError, requests.exceptions.JSONDecodeError):
        pass
    return [None, None]


if __name__ == "__main__":
    statcast_data = pd.read_parquet('../predictive_stuff_model/data/statcast.parquet')
    batted_balls = statcast_data[statcast_data['description'] == 'hit_into_play'].reset_index(drop=True)
    venue_cache = {}
    for game in batted_balls['game_pk'].unique():
        v_id, v_name = venue_identifier(game)
        venue_cache[int(game)] = {'venue_id': v_id, 'venue_name': v_name}
    with open('venue_cache.json', 'w') as f:
        json.dump(venue_cache, f, indent=4)
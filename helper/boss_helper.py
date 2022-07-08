import pandas as pd

boss_info = {
    'LUCID': {
        'EASY': {'lvl': 230, 'HP': [6000000000000, 6000000000000], 'defense': 300},
        'NORMAL': {'lvl': 230, 'HP': [12000000000000, 12000000000000], 'defense': 300},
        'HARD': {'lvl': 230, 'HP': [50800000000000, 54000000000000, 13200000000000], 'defense': 300}
    }
}

def get_boss_data(name):
    info = boss_info.get(name.upper())
    if not name:
        return None
    output_dict = {
        'HP':  [','.join([f'{hp/1000000000000}T' for hp in diff_list['HP']]) for diff_list in info.values()],
        'DEFENSE': [diff_list.get('defense', 'Unknown') for diff_list in info.values()],
        'LVL': [diff_list.get('lvl', 'Unknown') for diff_list in info.values()]
    }
    return pd.DataFrame.from_dict(output_dict, orient='index',
                       columns=info.keys())

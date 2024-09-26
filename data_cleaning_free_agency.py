import pandas as pd

def read_and_clean_data(filepath):
    #load in the dataframe
    # df = pd.read_csv('~/Desktop/Projects/MLB_2023/2023_player_data.csv')
    df = pd.read_csv(filepath)
    df.set_index('Rk', inplace=True)
    #remove the lg, obp, slg, ops, ops+ columns bc I will do them myself
    stats_df = df.drop(columns=['BA', 'Lg', 'OBP', 'SLG', 'OPS', 'OPS+'])

    #Remove all pitchers, I think they might be messing it up
    pitchers = []
    for index in stats_df.index:
        if str(stats_df.loc[index, 'Pos Summary']) in ["1", "/1", "1/H"]:
            pitchers.append(index)
    stats_df = stats_df.drop(pitchers)
    stats_df = stats_df.drop(849)
    stats_df.reset_index(drop=True, inplace=True)


    """
    for all players that played on multiple teams, have their combined stats
    as their stats for the whole season and replace their team with the team
    they ended the season on
    """

    indices_list = []
    index_to_keep = []
    for index in stats_df.index:
        if stats_df.loc[index, "Name-additional"] not in index_to_keep:
            index_to_keep.append(stats_df.loc[index, "Name-additional"])
        else:
            indices_list.append(index)

    """
    Getting the indices of the last team that every player 
    who played for multiple teams ended on
    """
    team_index = []
    index = 0
    while index < len(indices_list) - 1:
        current = indices_list[index]
        while (indices_list.index(current) + 1 < len(indices_list)) and \
            (current + 1 == indices_list[indices_list.index(current) + 1]):
            current += 1
        team_index.append(current)
        index = indices_list.index(current) + 1

    """Get the team name for every index"""
    team_name = []
    for i in team_index:
        team_name.append(stats_df.loc[i, 'Tm'])

    """implememnting all the neccessary changes"""
    modified_stats_df = stats_df.drop(indices_list)
    modified_stats_df.reset_index(drop=True, inplace=True)

    TOT_count = 0
    for i in modified_stats_df.index:
        if modified_stats_df.loc[i, 'Tm'] == 'TOT':
            TOT_count = TOT_count + 1
            modified_stats_df.loc[i, 'Tm'] = team_name.pop(0)

    """Changes the position column to the one that was played most"""
    def position_fix(position):
        for pos in str(position):
            if pos not in "*H/":
                return pos
        return None

    modified_stats_df["Pos Summary"] = \
            modified_stats_df["Pos Summary"].apply(position_fix)

    #Return the modified dataframe so that it can be used in the actual analyzer
    return modified_stats_df

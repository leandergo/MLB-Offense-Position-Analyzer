import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk

"""Load in the dataframe"""
player_stats = pd.read_csv("~/Desktop/Projects/MLB_2023/modified_stats.csv")

#League average stats !!NOT ROUNDED!!
league_ba = player_stats['H'].sum() / player_stats['AB'].sum()
league_obp_num = player_stats['H'].sum() + player_stats['BB'].sum() \
							+ player_stats['HBP'].sum()
league_obp_denom = player_stats['AB'].sum() + player_stats['BB'].sum() + \
						player_stats['HBP'].sum() + player_stats['SF'].sum()
league_obp = league_obp_num / league_obp_denom
league_slg = player_stats['TB'].sum() / player_stats['AB'].sum()
league_ops = league_obp + league_slg

#Get the OPS+ of a player
def get_OPS_plus(obp, slg):
	return round(100 * (obp/league_obp + slg/league_slg - 1))

#Grouping by position and adding the avg, obp, and slg
position_grouped = player_stats.groupby(by='Pos Summary').sum()\
		.drop(columns=["Unnamed: 0", "Name", "Age", "Tm", "Name-additional"])
position_grouped['Avg'] = round(position_grouped['H'] / \
								position_grouped['AB'], 3)

position_grouped['Obp'] = round((position_grouped['H'] + \
			position_grouped['BB'] + position_grouped['HBP']) / \
			(position_grouped['AB'] + position_grouped['BB'] + \
				position_grouped['HBP'] + position_grouped['SF']), 3)

position_grouped['Slg'] = round(position_grouped['TB'] / \
								position_grouped['AB'], 3)

position_grouped['OPS+'] = round(100 * (position_grouped['Obp']/league_obp + \
			 position_grouped['Slg']/league_slg - 1))
position_grouped['OPS+'] = position_grouped['OPS+'].astype(int)
# position_grouped.to_csv('testing.csv')

"""
This is the main function of the entire project
The point of this function is that the user inputs a team and then the function
will tell that person what postions need to get filled and what players would be
good fittings for that in free agency.
"""

def on_select(event=None):
    selected_team = dropdown.get()
    #Take the selected team and get the ops+ of all the postions
    team_group = player_stats.groupby(by = ['Tm', 'Pos Summary']).sum()\
    			.drop(columns=["Unnamed: 0", "Name", "Age", "Name-additional"])\
    			.reset_index()
    team_group.set_index('Tm', inplace = True)
    team_group = team_group.loc[team_group.index == selected_team]

    team_group['Avg'] = round(team_group['H'] / \
								team_group['AB'], 3)
    
    team_group['Obp'] = round((team_group['H'] + \
			team_group['BB'] + team_group['HBP']) / \
			(team_group['AB'] + team_group['BB'] + \
				team_group['HBP'] + team_group['SF']), 3)
    

    team_group['Slg'] = round(team_group['TB'] / \
								team_group['AB'], 3)
    

    team_group['OPS+'] = round(100 * (team_group['Obp']/league_obp + \
			 team_group['Slg']/league_slg - 1))
    

    team_group['OPS+'] = team_group['OPS+'].astype(int)
    team_group.reset_index()
    team_group.set_index('Pos Summary', inplace = True)
    team_group_OPS = team_group[['OPS+']]

    """    Create a relative stat that determines how good that teams
    player is to the average at that position
    This accounts for positions like first base who 
    tend to hit better than catchers
    ADJUST TO MAKE SURE THAT TEAMS WHERE A PLAYER DIDNT
    PLAY THE MAJORITY OF THEIR GAMES AT A CERTAIN POSITION
    GET ACCOUNTED FOR
    """
    
    team_positions = team_group.index.tolist()
    

    positions_of_team = position_grouped.loc[team_positions]
    team_group_OPS["Relative OPS+"] = team_group_OPS['OPS+'] / positions_of_team['OPS+']

    team_group_OPS = team_group_OPS.sort_values(by = 'Relative OPS+').reset_index()
    team_group_OPS.set_index('Pos Summary', inplace = True)
    
    top_3 = team_group_OPS.head(3).index.tolist()
    positions = []
    for position in top_3:
        if position == '2':
            positions.append("Catcher")
        elif position == '3':
            positions.append("First Base")
        elif position == '4':
            positions.append("Second Base")
        elif position == '5':
            positions.append("Third Base")
        elif position == '6':
            positions.append("Shortstop")
        elif position == '7':
            positions.append("Left Field")
        elif position == '8':
            positions.append("Center Field")
        elif position == '9':
            positions.append("Right Field")
        elif position == 'D':
            positions.append("Designated Hitter")

    print("The top 3 positions that need to be filled are:")
    print(positions)
    # pos_ops = position_grouped['OPS+'].tolist()
    # team_group['Pos OPS+'] = team_group['OPS+'] / pos_ops
    # team_group = team_group.sort_values(by = 'Pos OPS+').reset_index()
    # team_group.set_index('Pos Summary', inplace = True)


    # for index in team_group.index:
    # 	if position['Pos OPS+']
    # team_group.to_csv('testing.csv')



# Create the main window
root = tk.Tk()
root.title("Select Team")

# Create a label
label = tk.Label(root, text="Select a baseball team:")
label.pack(pady=10)

# Create a dropdown menu
teams = ["ARI", "ATL", "BOS", "CHC", "CHW", "CIN", "CLE", "COL", "DET", \
"MIA", "HOU", "KCR", "LAA", "LAD", "MIL", "MIN", "NYM", "NYY", "OAK", \
"PHI", "PIT", "SDP", "SFG", "SEA", "STL", "TBR", "TEX", "TOR", "WAS"]
dropdown = ttk.Combobox(root, values=teams)
dropdown.pack()

# Set default team
dropdown.set(teams[0])

# Bind the dropdown to a function
dropdown.bind("<<ComboboxSelected>>", on_select)

# Run the application
root.mainloop()
# print(get_OPS_plus(.400, .500))

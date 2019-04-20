"""
This script runs a sweep over a specified range of wagers
The output is num_sweeps x num_sims
Each row represents the simulations run for a particular wager
"""

import numpy as np
from cleoslots.slots_models import CleopatraModel

load_file = False
filename = '../output/sweep_fixed_wager.npz'

costs = np.linspace(.05, 0.3, 26)  # from a 5 cent bet to a 30 cent bet
num_sweeps = len(costs)

spending_money_initial = 40
walk_away_win = 10
nlines = 1  # 1 line Cleopatra

transition_time = 30  # number of seconds spent switching machines

num_hours = 3
time_max = 60 * 60 * num_hours

num_sims = 1000

# money = num_intervals x num_sims
avg_won = np.zeros((num_sweeps, num_sims))
avg_time = np.zeros_like(avg_won)
avg_spent = np.zeros_like(avg_won)
avg_plays = np.zeros_like(avg_won)

cleo = CleopatraModel(nlines=nlines)

for i, cost_per_bet in enumerate(costs):
    max_loss_per_session = 3 * cost_per_bet
    for j in range(num_sims):
        spending_money = spending_money_initial
        time_played = 0
        total_won = 0
        total_spent = 0
        total_num_games = 0
        while spending_money > cost_per_bet and time_played < time_max:
            time_played += transition_time
            output = cleo.one_session(spending_money, cost_per_bet, max_loss_per_session, time_max - time_played,
                                      walk_away_win)
            total_num_games += output[0]
            time_played += output[0] * cleo.time_per_spin
            total_won += output[1]
            total_spent += output[2]
            spending_money += output[1] - output[2]
        avg_won[i, j] = total_won
        avg_time[i, j] = time_played
        avg_plays[i, j] = total_num_games
        avg_spent[i, j] = total_spent

# save to file
np.savez(filename, avg_won=avg_won, avg_time=avg_time, avg_plays=avg_plays, avg_spent=avg_spent)
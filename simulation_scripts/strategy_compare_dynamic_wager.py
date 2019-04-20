"""
This script allows one to simulate multiple trips to the casino with a single strategy
Our wagers here are DYNAMIC, so we may change our bet size depending on how much we win
The saved output is 2 x number of simulations
Row 1: Lori's results
Row 2: Ben's results
"""

import numpy as np
from cleoslots.slots_models import CleopatraModel

filename = '../output/strategy_compare_dynamic_wager.npz'

# Initial/default wager
cost_per_bet = [0.3, 0.3]

change_bet_win = [30, 30]  # this is the key that makes our wagers dynamic; if we're up 30 bucks, change to winning_bet
winning_bet = [0.5, 0.1]  # Lori bets 30 cents more, I bet 20 cents less

max_loss_per_session = [np.inf, 3 * cost_per_bet[1]]
spending_money_initial = [100, 100]
walk_away_win = [10, 10]

transition_time = 30  # number of seconds spent switching machines

num_hours = 3
time_max = 60 * 60 * num_hours

num_sims = 1000
nlines=20

# money = num_intervals x num_sims
avg_won = np.zeros((2, num_sims))
avg_time = np.zeros_like(avg_won)
avg_spent = np.zeros_like(avg_won)
avg_plays = np.zeros_like(avg_won)

cleo = CleopatraModel(nlines=nlines)

for i in range(2):
    for j in range(num_sims):
        wager = cost_per_bet[i]
        spending_money = spending_money_initial[i]
        time_played = 0
        total_won = 0
        total_spent = 0
        total_num_games = 0
        while spending_money > cost_per_bet[i] and time_played < time_max:
            time_played += transition_time
            output = cleo.one_session(spending_money, wager, max_loss_per_session[i], time_max - time_played,
                                      walk_away_win[i], initial_money=spending_money_initial[i],
                                      winning_bet=winning_bet[i], change_bet_win=change_bet_win[i])
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
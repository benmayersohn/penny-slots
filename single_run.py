# Lori and I both gamble for three hours with different strategies.
# How well do we do?

import numpy as np
from slots_models import CleopatraModel
import matplotlib.pyplot as plt
import seaborn as sns

load_file = False

cost_per_bet = [0.3]

# max_loss_per_session = [np.inf, 3 * cost_per_bet[1]]
# spending_money_initial = [100, 40]
# walk_away_win = [10, 5]

max_loss_per_session = [np.inf]
spending_money_initial = [np.inf]
walk_away_win = [np.inf]

transition_time = 30  # number of seconds spent switching machines

num_hours = 30
time_max = 60 * 60 * num_hours

num_sims = 10

# money = num_intervals x num_sims
avg_won = np.zeros((1, num_sims))
avg_time = np.zeros_like(avg_won)
avg_spent = np.zeros_like(avg_won)
avg_plays = np.zeros_like(avg_won)

cleo = CleopatraModel(nlines=1)

i=0
for j in range(num_sims):
    spending_money = spending_money_initial[i]
    time_played = 0
    total_won = 0
    total_spent = 0
    total_num_games = 0
    while spending_money > cost_per_bet[i] and time_played < time_max:
        time_played += transition_time
        output = cleo.one_session(spending_money, cost_per_bet[i], max_loss_per_session[i], time_max - time_played,
                                  walk_away_win[i])
        total_num_games += output[0]
        time_played += output[0] * cleo.time_per_spin
        total_won += output[1]
        total_spent += output[2]
        spending_money += total_won - total_spent
    avg_won[i, j] = total_won
    avg_time[i, j] = time_played
    avg_plays[i, j] = total_num_games
    avg_spent[i, j] = total_spent
    print('win: {}, lose: {}'.format(total_won, total_spent))

avg_money = avg_won - avg_spent

won = np.mean(avg_won, axis=1)
time = np.mean(avg_time, axis=1)
plays = np.mean(avg_plays, axis=1)
spent = np.mean(avg_spent, axis=1)

pct_remaining = 100 * won / spent

print(r'On average, you made back {}% of what you spent.'.format(pct_remaining[0]))
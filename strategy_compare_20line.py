# Lori and I both gamble for three hours with different strategies.
# How well do we do?

import numpy as np
from slots_models import CleopatraModel
import matplotlib.pyplot as plt
import seaborn as sns

load_file = True
filename = 'strategies_20line_diffstart_ben1.npz'

# Lori is strategy 1, Ben is strategy 2
cost_per_bet = [0.3, 0.01]

max_loss_per_session = [np.inf, 3 * cost_per_bet[1]]
spending_money_initial = [100, 40]
walk_away_win = [10, 10]

transition_time = 30  # number of seconds spent switching machines

num_hours = 3
time_max = 60 * 60 * num_hours

num_sims = 1000

# money = num_intervals x num_sims
avg_won = np.zeros((2, num_sims))
avg_time = np.zeros_like(avg_won)
avg_spent = np.zeros_like(avg_won)
avg_plays = np.zeros_like(avg_won)

# the return can be represented as avg_won/avg_spent * 100
if load_file:
    results = np.load(filename)
    avg_won = results['avg_won']  # total won; positive number
    avg_time = results['avg_time']
    avg_plays = results['avg_plays']
    avg_spent = results['avg_spent']  # total spent; positive number
else:
    cleo = CleopatraModel()

    for i in range(2):
        for j in range(num_sims):
            spending_money = spending_money_initial[i]
            time_played = 0
            total_won = 0
            total_spent = 0
            total_num_games = 0
            while spending_money > cost_per_bet[i] and time_played < time_max:
                time_played += transition_time
                output = cleo.one_session(spending_money, cost_per_bet[i], max_loss_per_session[i],
                                          time_max - time_played, walk_away_win[i])
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



'''
avg_money = avg_won - avg_spent

won = np.mean(avg_won, axis=1)
time = np.mean(avg_time, axis=1)
plays = np.mean(avg_plays, axis=1)
spent = np.mean(avg_spent, axis=1)

pct_remaining = 100 * np.mean(avg_won / avg_spent, axis=1)

avg_utility = avg_won / avg_spent * np.exp((avg_time - time_max)/avg_time)
utility = np.mean(avg_utility, axis=1)

print(r'On average, Lori made back {}% of what she spent.'.format(pct_remaining[0]))
print(r'On average, Ben made back {}% of what he spent.'.format(pct_remaining[1]))

print('On average, Lori\'s utility is {}.'.format(utility[0]))
print('On average, Ben\'s utility is {}.'.format(utility[1]))


fig, ax = plt.subplots(1, 1)
ax.hist(avg_money[0, :], rwidth=1, normed=True, label='Lori', alpha = 0.7)
ax.set_title('Earnings Distribution')
ax.set_ylabel('Frequency')
ax.set_xlabel('Earnings')
ax.hist(avg_money[1, :], rwidth=1, normed=True, label='Ben', alpha = 0.7)
ax.legend()

plt.show()
'''
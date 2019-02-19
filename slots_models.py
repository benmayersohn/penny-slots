# A model of the Cleopatra slot machine
# Data from Wizard of Odds (https://wizardofodds.com/games/slots/cleopatra/)
# and Casino Guru (https://casino.guru/cleopatra-slot-math)

import numpy as np
import scipy.stats as st


# Generic slots class
class SlotsModel(object):
    '''
    intervals: intervals corresponding to categories of win, as multiple of input $
    probabilities: probability of falling in corresponding interval
    name: Name of slots machine
    model: constructed from intervals/probabilities
    '''
    def __init__(self, name, intervals, probabilities, time_per_spin):
        self.intervals = intervals
        self.name = name
        self.probabilities = probabilities
        self.time_per_spin = time_per_spin
        self.model = None

    def construct_model(self):
        self.model = st.rv_discrete(name=self.name, values=(np.arange(len(self.probabilities)), self.probabilities))

    def one_play(self, cost_per_bet):

        if self.model is None:
            self.construct_model()

        index = self.model.rvs()
        if index == 0:
            return 0

        interval = self.intervals[index]
        winnings = cost_per_bet * (interval[0] + st.uniform.rvs() * (interval[1] - interval[0]))
        return winnings

    def one_session(self, money_in, wager, max_loss_per_session, time_limit, walk_away_win, wager_type='absolute',
    initial_money=None, winning_bet=None, change_bet_win=None):

        def wager_calc(w, money):
           return w if wager_type == 'absolute' else max(.01, w * money)

        total_won = 0
        total_spins = 0
        total_spent = 0
        time_elapsed = 0
        net = 0
        spending_money = money_in
        betting_higher = False

        cost_per_bet = wager_calc(wager, spending_money)

        while net + max_loss_per_session > 0 and spending_money > cost_per_bet and time_elapsed < time_limit:
            result = self.one_play(cost_per_bet)
            time_elapsed += self.time_per_spin
            total_spins += 1
            total_won += result
            total_spent += cost_per_bet
            net = total_won - total_spent
            spending_money += net

            # if you want to change your wager when exceeding a threshold, and change it back when you're down again
            if None not in (change_bet_win, winning_bet, initial_money):
                if money_in + net >= initial_money + change_bet_win and not betting_higher:
                    betting_higher = True
                if money_in + net < initial_money and betting_higher:
                    betting_higher = False

                cost_per_bet = wager_calc(winning_bet if betting_higher else wager, spending_money)
            else:
                cost_per_bet = wager_calc(wager, spending_money)  # recalculate wager based on spending money

            if result > walk_away_win:
                return total_spins, total_won, total_spent

        return total_spins, total_won, total_spent


class CleopatraModel(SlotsModel):
    def __init__(self, nlines=20):
        self.name = 'cleopatra'
        if nlines == 20:
            self.intervals = np.array([
                [0., 0.2],
                [0.2, 0.5],
                [0.5, 1.],
                [1., 2.],
                [2., 5.],
                [5., 10.],
                [10., 20.],
                [20., 50.],
                [50., 100.],
                [100., 200.],
                [200., 500.],
                [500., 1000.]
            ])

            # Payout is 95.025%
            self.probabilities = 0.7987446566693283 * np.array(
            [929482, 740452, 563289, 1031867, 149001, 92050, 58006, 17450, 3538, 505, 20]
            ) / 10000000.
        elif nlines == 1:
            self.intervals = np.array([
                [0., 2.],
                [2., 5.],
                [5., 10.],
                [10., 20.],
                [20., 50.],
                [50., 100.],
                [100., 200.],
                [200., 500.],
                [500., 1000.],
                [1000., 2000.],
                [2000., 5000.],
                [5000., 10000.],
                [10000., 20000.]
            ])

            # Payout is 95.025%
            self.probabilities = 0.7233308569575265 * np.array(
            [8761210, 628815, 1008567, 544354, 273149, 82322, 52222, 8952, 1532, 411, 21, 6]
            ) / 100000000.
        self.probabilities = np.array([1-np.sum(self.probabilities), *self.probabilities])
        self.model = None
        self.time_per_spin = 5

import numpy as np
from numpy.random import default_rng
from decimal import *


class Algorithm:
    """
    Basic framework for online algorithms for the Two-Way Trading Problem.
    Precise online algorithms will be defined as subclasses of this class.
    Subclasses need to provide an implementation of the function trade(self, exchange_rate).
    ...

    Attributes
    ----------
    state : integer in {0, 1}
        Current state.
    payoff : float
        Payoff accumulated by the algorithm so far.
    x : integer in {-1, 0, 1}
        Current trade decision.
        x == 0: do not trade
        x == 1: buy
        x == -1: sell

    Methods
    -------
    run(self, exchange_rate)
        Executes one step of the algorithm: Trades as specified in x and updates the state and accumulated payoff accordingly.

    trade(self, exchange_rate)
        Sets self.x. The function is not implemented in this class
        as it will be overwritten by the corresponding function in the subclasses.

    update_state(demand)
        Updates the state of the algorithm based on the current state and self.x.

    update_payoff(price)
        Multiplies the current payoff wih the current gain.
    """
    def __init__(self, k):
        self.state = 0
        self.payoff = 1
        self.x = 0
        self.k = k
        self.count_trade = 0

    def run(self, exchange_rate):
        if self.count_trade < self.k:
            self.trade(exchange_rate)
            self.correct_trade()
            self.update_payoff(exchange_rate)
            self.update_state()
            if self.x == -1:  # TODO
                self.k += 1

    def run_last(self, exchange_rate):
        self.x = -1
        self.correct_trade()
        self.update_payoff(exchange_rate)
        self.update_state()

    def trade(self, exchange_rate):
        """
        Placeholder function for implementations in subclasses.
        """
        pass

    def correct_trade(self):
        """
        Correct invalid transactions.
        If we want to buy but the next possible action is to sell, then we will do nothing.
        Similarly if we want to sell but the next allowed transaction is to buy, we will also do nothing.
        """
        if self.x == 1 and self.state == 1:
            # print("Cannot buy. Remain in state 'sell'.")
            self.x = 0
        elif self.x == -1 and self.state == 0:
            # print("Cannot sell. Remain in state 'buy'.")
            self.x = 0

    def update_payoff(self, exchange_rate):
        if self.state == 0 and self.x == 1:
            self.payoff /= exchange_rate
        elif self.state == 1 and self.x == -1:
            self.payoff *= exchange_rate
        else:
            pass

    def update_state(self):
        self.state = np.clip(self.state + self.x, 0, 1)


class AlgorithmPred(Algorithm):
    """
    This is the class of online algorithms with predictions.
    The predictions used here tell the algorithm whether to buy, sell or do nothing in the current step.

    Attributes
    ----------
    prediction : integer in {-1, 0, 1}
        Prediction for the current time step.
    remaining_predictions : list
        List of predictions for the time steps remaining from the current time step on.

    Methods
    -------
    update_prediction()
        Gets the next entry from the list of the remaining predicitions and stores it in self.predicition.
        The value is removed from the list.

    """
    def __init__(self, k, predictions):
        super().__init__(k)
        self.prediction = 0
        self.remaining_predictions = predictions.copy()
        self.remaining_predictions.reverse()  # reverse the list to be able to pop first element from list

    def update_prediction(self):
        self.prediction = self.remaining_predictions.pop()

# TODO: implement second class for algorithms with predictions, where the predictions are of the type "trade" or no "trade"


class AlgorithmRandom(Algorithm):
    """
    This is the class of online algorithms for the Two-Way Trading problem where one of the actions "b", "s", "0"
    is drawn uniformly at random in every step.

    Attributes
    ----------
    No additional attributes besides the attributes defined in the super class Algorithm.

    Methods
    -------
    trade(phi, price, demand)
        Sets self.x to a value uniformly drawn from [-1, 0, 1].

    """

    def __init__(self, k):
        super().__init__(k)

    def trade(self, exchange_rate):
        rng = default_rng()

        self.x = rng.integers(-1, 1, endpoint=True)


class AlgorithmRandomTrade(Algorithm):
    """
    This is the class of online algorithms for the Two-Way Trading problem where the decision whether to trade or not
    is made uniformly at random in every time step.

    Attributes
    ----------
    No additional attributes besides the attributes defined in the super class Algorithm.

    Methods
    -------
    trade(phi, price, demand)
        Draws a value "trade" uniformly at random from [0, 1].
        Sets self.x to one of the possibilities [-1, 0, 1], depending on the current state and the value drawn above
            - if trade == 0: do nothing
            - if trade == 1:
                * if self.state == 0: self.x = 1
                * if self.state == 1: self.x = -1
    """

    def __init__(self, k):
        super().__init__(k)

    def trade(self, exchange_rate):
        rng = default_rng()

        trade = rng.integers(0, 1, endpoint=True)
        if trade == 0:
            self.x = 0
        else:
            if self.state == 0:
                self.x = 1
            else:
                self.x = -1


class FtP(AlgorithmPred):
    """
    Implementation of the Follow-the-Prediction algorithm that gets exact transaction types as predictions,
    i.e. -1, 0, or 1, as input.
    """
    def trade(self, exchange_rate):
        self.update_prediction()
        self.x = self.prediction


class FtPTrade(AlgorithmPred):
    """
    Implementation of the Follow-the-Prediction algorithm that just gets the information whether or not to trade,
    i.e. 0 (no trade) or 1 (trade) as input.
    """
    def trade(self, exchange_rate):
        self.update_prediction()
        if self.state == 0:
            self.x = self.prediction
        else:
            self.x = -self.prediction


class CombineRandStart(Algorithm):
    def __init__(self, k, alg0, alg1, l):
        super().__init__(k)
        self.l = l
        rng = np.random.default_rng()
        self.index = rng.choice([0, 1], 1, p=[l, 1-l])
        if self.index == 0:
            self.followed_alg = alg0
            self.other_alg = alg1
        else:
            self.followed_alg = alg1
            self.other_alg = alg0

    def trade(self, exchange_rate):
        self.followed_alg.trade(exchange_rate)
        self.other_alg.trade(exchange_rate)
        self.x = self.followed_alg.x


class CombineRandStep(Algorithm):
    def __init__(self, k, alg0, alg1, l):
        super().__init__(k)
        self.l = l
        self.alg0 = alg0
        self.alg1 = alg1

    def trade(self, exchange_rate):
        rng = np.random.default_rng()
        index = rng.choice([0, 1], 1, p=[self.l, 1 - self.l])
        self.alg0.trade(exchange_rate)
        self.alg1.trade(exchange_rate)
        if index == 0:
            self.x = self.alg0.x
        else:
            self.x = self.alg1.x


class OptDeterministic(Algorithm):

    def __init__(self, k, phi):
        super().__init__(k)
        self.phi = phi

    def trade(self, exchange_rate):
        if exchange_rate <= self.phi**(1/3):
            self.x = 1
        elif exchange_rate >= self.phi**(2/3):
            self.x = -1
        else:
            self.x = 0



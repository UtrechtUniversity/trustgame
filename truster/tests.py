from . import *
from otree.api import Currency as cu

class PlayerBot(Bot):
    def play_round(self):
        yield Send, {'sent_amount': C.ENDOWMENT / 2}

from otree.api import *

doc = """
Trust Game – Player A decides how many points to send to B
"""

class C(BaseConstants):
    NAME_IN_URL = 'trust_A'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10)
    MULTIPLICATION_FACTOR = 3


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    sent_amount = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,
        label="How much do you want to send?"
    )

class SendPage(Page):
    form_model = 'player'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars.get('role') == 'A'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['sent_amount'] = player.sent_amount

page_sequence = [SendPage]

from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'truster'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10)
    MULTIPLICATION_FACTOR = 3

class Subsession(BaseSubsession): pass
class Group(BaseGroup): pass

class Player(BasePlayer):
    sent_amount = models.CurrencyField(min=0, max=C.ENDOWMENT, label="")

class Send(Page):
    form_model = 'player'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars.get('role') == 'A'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(endowment=C.ENDOWMENT)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['sent_amount'] = player.sent_amount
        print(f"[DEBUG][truster] A#{player.participant.id_in_session} sent={player.sent_amount}")

page_sequence = [Send]

from otree.api import *

doc = """
Trust Game – Player B decides how much to send back to Player A.
"""

class C(BaseConstants):
    NAME_IN_URL = 'trust_B'
    PLAYERS_PER_GROUP = 2  # grouping happens here
    NUM_ROUNDS = 1
    MULTIPLICATION_FACTOR = 3
    ENDOWMENT = cu(10)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    sent_amount = models.CurrencyField()
    sent_back_amount = models.CurrencyField(
        label="How much do you want to send back?",
        min=0
    )

def set_payoffs(group: Group):
    p1 = group.get_player_by_role('A')
    p2 = group.get_player_by_role('B')
    p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount
    p2.payoff = group.sent_amount * C.MULTIPLICATION_FACTOR - group.sent_back_amount

class Player(BasePlayer):
    def role(self):
        return self.participant.vars['role']

class GroupWaitPage(WaitPage):
    title_text = "Please wait ..."
    body_text = "You are <strong>Player B</strong>. Please wait while Player A decides how many points to send you."

    group_by_arrival_time = True

    @staticmethod
    def after_all_players_arrive(group: Group):
        # get Player A's previous choice
        p1 = group.get_player_by_role('A')
        group.sent_amount = p1.participant.vars['sent_amount']

class SendBack(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.role() == 'B'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            sent_amount=player.group.sent_amount,
            tripled_amount=player.group.sent_amount * C.MULTIPLICATION_FACTOR
        )

class ResultsWaitPage(WaitPage):
    title_text = "Please wait ..."
    body_text = "Please wait while Player B decides how many points to return to you."
    after_all_players_arrive = set_payoffs

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        sent = group.sent_amount
        returned = group.sent_back_amount
        multiplier = C.MULTIPLICATION_FACTOR

        if player.participant.vars['role'] == 'A':
            return dict(
                role='A',
                sent_amount=sent,
                tripled_amount=sent * multiplier,
                returned_amount=returned,
                received_back=returned,
                payoff=player.payoff,
                multiplier=multiplier
            )
        else:
            return dict(
                role='B',
                sent_amount=sent,
                received_amount=sent * multiplier,
                sent_back=returned,
                payoff=player.payoff,
                multiplier=multiplier
            )

class Exit(Page):
    pass


page_sequence = [GroupWaitPage, SendBack, ResultsWaitPage, Results, Exit]

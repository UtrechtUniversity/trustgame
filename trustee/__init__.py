from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'trustee'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    MULTIPLIER = 3
    ENDOWMENT = cu(10)

class Subsession(BaseSubsession): pass

def group_by_arrival_time_method(subsession: Subsession, waiting_players):
    a_waiting = [p for p in waiting_players
                 if p.participant.vars.get('role') == 'A'
                 and p.participant.vars.get('sent_amount') is not None]

    b_waiting = [p for p in waiting_players if p.participant.vars.get('role') == 'B']

    if a_waiting and b_waiting:
        a = a_waiting[0]
        b = b_waiting[0]
        print(f"[DEBUG][trustee] Pairing A#{a.participant.id_in_session} ↔ B#{b.participant.id_in_session}")
        return [a, b]

    return None

class Group(BaseGroup):
    sent_back_amount = models.CurrencyField(min=0, label="", null=True, blank=True)

    def set_payoffs(self):
        a = self.get_player_by_role('A')
        b = self.get_player_by_role('B')

        sent = a.participant.vars.get('sent_amount', cu(0))

        sent_back = self.field_maybe_none('sent_back_amount') or cu(0)

        a.payoff = C.ENDOWMENT - sent + sent_back
        b.payoff = sent * C.MULTIPLIER - sent_back

        print(f"[DEBUG][trustee][payoffs] A sent={sent}, back={sent_back} | "
              f"A.payoff={a.payoff}, B.payoff={b.payoff}")

class Player(BasePlayer):

    def role(self):
        return self.participant.vars.get('role')


class MatchWait(WaitPage):
    group_by_arrival_time = True
    title_text = "Please wait"
    body_text = "You will be paired with another player ..."

class SendBack(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    @staticmethod
    def is_displayed(player: Player):
        # Only displayed for B, and only if A actually sent something
        if player.role() != 'B':
            return False
        a = player.group.get_player_by_role('A')
        sent = a.participant.vars.get('sent_amount', cu(0))
        return sent > 0

    @staticmethod
    def vars_for_template(player: Player):
        a = player.group.get_player_by_role('A')
        sent = a.participant.vars['sent_amount']
        return dict(sent=sent, tripled=sent * C.MULTIPLIER)

    @staticmethod
    def error_message(player: Player, values):
        """Ensure B cannot send back more than received."""
        a = player.group.get_player_by_role('A')
        sent = a.participant.vars.get('sent_amount', cu(0))
        tripled = sent * C.MULTIPLIER

        if values['sent_back_amount'] > tripled:
            return f"You cannot send back more than {tripled}."

class AWait(WaitPage):
    # A waits for Bs decision
    @staticmethod
    def is_displayed(player: Player):
        return player.role() == 'A'

class ResultsWait(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_payoffs()

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        a = player.group.get_player_by_role('A')
        sent = a.participant.vars['sent_amount']
        return dict(
            role=player.role(),
            sent=sent,
            tripled=sent * C.MULTIPLIER,
            sent_back = player.group.field_maybe_none('sent_back_amount') or cu(0),
            payoff=player.payoff,
        )

class Exit(Page):
    pass

page_sequence = [MatchWait, SendBack, AWait, ResultsWait, Results, Exit]

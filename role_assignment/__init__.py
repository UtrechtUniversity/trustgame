from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'role_assignment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    def creating_session(self):
        self.session.vars.setdefault('n_joined', 0)

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass

class Introduction(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        n = player.session.vars.get('n_joined', 0)
        role = 'A' if n % 2 == 0 else 'B'
        player.participant.vars['role'] = role
        player.session.vars['n_joined'] = n + 1
        print(f"[DEBUG][role_assignment] P#{player.participant.id_in_session} -> role={role}")

page_sequence = [Introduction]

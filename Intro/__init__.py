from otree.api import *

doc = """
Instruction to the game.
When players proceed to the game, they are assigned a role (alternating player A/B)
"""

class C(BaseConstants):
    NAME_IN_URL = 'Introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10)
    MULTIPLICATION_FACTOR = 3

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    role_assigned = models.StringField()

class Introduction(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            endowment=C.ENDOWMENT,
            multiplier=C.MULTIPLICATION_FACTOR,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # initialize counter if not yet present
        if 'role_counter' not in player.session.vars:
            player.session.vars['role_counter'] = 0

        # read current counter into a local variable
        current_counter = player.session.vars['role_counter']

        # assign role based on counter (even -> A, odd -> B)
        if current_counter % 2 == 0:
            role = 'A'
            parity = 'even'
        else:
            role = 'B'
            parity = 'odd'

        # increment counter
        player.session.vars['role_counter'] = current_counter + 1

        # save role
        player.role_assigned = role
        player.participant.vars['role'] = role
        player.participant.vars['endowment'] = C.ENDOWMENT
        player.participant.vars['multiplier'] = C.MULTIPLICATION_FACTOR

        # debugging prints
        #pid = player.participant.id_in_session
        #print(f"[DEBUG] Participant id_in_session={pid} | "
        #      f"player_counter={current_counter} | parity={parity} | assigned_role={role}")

page_sequence = [Introduction]

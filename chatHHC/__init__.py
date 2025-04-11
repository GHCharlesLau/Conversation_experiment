from otree.api import *
import json


doc = """
Of course oTree has a readymade chat widget described here: 
https://otree.readthedocs.io/en/latest/multiplayer/chat.html

But you can use this if you want a chat box that is more easily customizable,
or if you want programmatic access to the chat messages. 

This app can also help you learn about live pages in general.
"""


class C(BaseConstants):
    NAME_IN_URL = 'chat_H'
    PLAYERS_PER_GROUP = 2  # All players are in the same group or it's a single-player game if this is None.
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    HHC = models.BooleanField(default=True)
    chatLog = models.LongStringField(blank=True)

    num_messages = models.IntegerField(initial=0)
    chat_finished = models.BooleanField(initial=False)


class Message(ExtraModel):
    group = models.Link(Group)
    sender = models.Link(Player)
    text = models.StringField()


def to_dict(msg: Message):
    return dict(sender=msg.sender.id_in_group, text=msg.text)


# PAGES
class pairingSuc(Page):
    @staticmethod
    def vars_for_template(player: Player):
        alter = player.get_others_in_group()[0]
        return dict(
                    alter_id = alter.id_in_group,
                    alter_nickname=alter.participant.nickname,
                    alter_avatar=alter.participant.avatar,
                    )

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.partnership == 'HHC'


class chatEmo(Page):
    form_model = 'player'
    form_fields = ['chatLog']
    timeout_seconds = 1200
    
    @staticmethod
    def js_vars(player: Player):
        alter = player.get_others_in_group()[0]
        return dict(my_id=player.id_in_group,
                    my_code=player.participant.code,
                    my_nickname=player.participant.nickname,
                    my_avatar=player.participant.avatar,
                    alter_code=alter.participant.code,
                    alter_nickname=alter.participant.nickname,
                    alter_avatar=alter.participant.avatar,
                    )

    @staticmethod
    def vars_for_template(player: Player):
        alter = player.get_others_in_group()[0]
        return dict(
                    my_avatar=player.participant.avatar,
                    alter_avatar=alter.participant.avatar,
                    )

    @staticmethod
    def live_method(player: Player, data):
        player.num_messages += 1
        my_id = player.id_in_group
        group = player.group

        if data["text"] == "user_exited":
            response = dict(
                text="user_exited",
            )
            return {0: response}  # Broadcast to all players
        elif player.num_messages > 16:  # set maximum number of turns (should be plus 1 based on the number of turns)
            player.chat_finished = True
            response = dict(
                text="chat_exceeded",
            )
            # return {player.id_in_group: response['text']}
            return {0: response}
        else:
            if 'text' in data:
                text = data['text']
                msg = Message.create(group=group, sender=player, text=text)
                return {0: [to_dict(msg)]}
        return {my_id: [to_dict(msg) for msg in Message.filter(group=group)]}
    
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.taskType == 'emotionTask' and player.participant.partnership == 'HHC'


class chatFun(Page):
    form_model = 'player'
    form_fields = ['chatLog']
    timeout_seconds = 1200
    
    @staticmethod
    def js_vars(player: Player):
        alter = player.get_others_in_group()[0]
        return dict(my_id=player.id_in_group,
                    my_code=player.participant.code,
                    my_nickname=player.participant.nickname,
                    my_avatar=player.participant.avatar,
                    alter_code=alter.participant.code,
                    alter_nickname=alter.participant.nickname,
                    alter_avatar=alter.participant.avatar,
                    )

    @staticmethod
    def vars_for_template(player: Player):
        alter = player.get_others_in_group()[0]
        return dict(
                    my_avatar=player.participant.avatar,
                    alter_avatar=alter.participant.avatar,
                    )

    @staticmethod
    def live_method(player: Player, data):
        player.num_messages += 1
        my_id = player.id_in_group
        group = player.group

        if data["text"] == "user_exited":
            response = dict(
                text="user_exited",
            )
            return {0: response}  # Broadcast to all players
        elif player.num_messages > 16:  # set maximum number of turns (should be plus 1 based on the number of turns)
            player.chat_finished = True
            response = dict(
                text="chat_exceeded",
            )
            # return {player.id_in_group: response['text']}
            return {0: response}
        else:
            if 'text' in data:
                text = data['text']
                msg = Message.create(group=group, sender=player, text=text)
                return {0: [to_dict(msg)]}
        return {my_id: [to_dict(msg) for msg in Message.filter(group=group)]}
    
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.taskType == 'functionTask' and player.participant.partnership == 'HHC'


# WaitPage Messages
# chatInstruct_emo_human
body_textA = '''
<p>Please wait for your partner to arrive.</p>
'''

# chatInstruct_fun_human
body_textB = '''
<p>Please wait for your partner to arrive.</p>
'''

# Setting a WaitPage to group_by_arrival_time=True
class MyWaitPage(WaitPage):
    group_by_arrival_time = True
    # title_text = "Waiting..."
    # body_text = "Waiting for other participants to join..."
    template_name = 'chatHHC/MyWaitPage.html'
    timeout_seconds = 120
    form_model = 'player'
    form_fields = ['HHC']

    @staticmethod
    def vars_for_template(player):
        if player.participant.taskType == 'emotionTask' and player.participant.partnership == 'HHC':
            return dict(body_text=body_textA)
        elif player.participant.taskType == 'functionTask' and player.participant.partnership == 'HHC':
            return dict(body_text=body_textB)
        else:
            pass

    @staticmethod
    def is_displayed(player):
        return player.participant.partnership == 'HHC'

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            # you may want to fill a default value for any form fields,
            # because otherwise they may be left null.
            player.HHC = False
            player.participant.partnership = "HMC"  # If timeout happened, the subject should be assigned to a chat room with a bot.
    @staticmethod
    def app_after_this_page(player, upcoming_apps):  # If waiting too long, the subject should be assigned to a chat room with a bot.
        print('upcoming_apps is', upcoming_apps)
        if player.HHC == False:
            return "chatHMC"
        

def waiting_too_long(player):
    participant = player.participant

    import time
    # assumes you set wait_page_arrival in PARTICIPANT_FIELDS.
    return time.time() - participant.wait_page_arrival > 120


def group_by_arrival_time_method(subsession, waiting_players):
    # Confine the group by taskType
    emo_players = [p for p in waiting_players if p.participant.taskType == 'emotionTask' and p.participant.partnership == 'HHC']
    fun_players = [p for p in waiting_players if p.participant.taskType == 'functionTask' and p.participant.partnership == 'HHC']

    if len(emo_players) >= 2:
        print('emo_players is', emo_players)
        return [emo_players[0], emo_players[1]]
    elif len(fun_players) >= 2:
        print('fun_players is', fun_players)
        return [fun_players[0], fun_players[1]]
    else:
        pass

    if len(waiting_players) >= 2:
        return waiting_players[:2]
    for player in waiting_players:
        if waiting_too_long(player):
            player.HHC = False  # If timeout happened, the subject should be re-assigned to the chatHMC group.
            player.participant.partnership = "HMC"
            # make a single-plEmoayer group.
            return [player]


# custom export of chatLog
def custom_export(players):
    # header row
    yield ['session_code', 'participant_code', 'nickname', 'taskType', 'partnership', 'sender', 'text', 'timestamp']
    for p in players:
        participant = p.participant
        session = p.session

        # expand chatLog
        log = p.field_maybe_none('chatLog')
        if log:    
            json_log = json.loads(log)
            print(json_log)
            for r in json_log:
                sndr = r['sender']
                txt = r['text']
                time = r['timestamp']
                yield [session.code, participant.code, participant.vars.get('nickname', None), participant.vars.get('taskType', None), participant.vars.get('partnership', None), sndr, txt, time]


page_sequence = [MyWaitPage, pairingSuc, chatEmo, chatFun]

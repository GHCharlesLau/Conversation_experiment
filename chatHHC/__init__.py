from otree.api import *


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
                    alther_code=alter.participant.code,
                    alter_nickname=alter.participant.nickname,
                    alter_avatar=alter.participant.avatar,
                    )

    @staticmethod
    def live_method(player: Player, data):
        my_id = player.id_in_group
        group = player.group

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
    def live_method(player: Player, data):
        my_id = player.id_in_group
        group = player.group

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
<p>1. You will be paired with a participant in this survey. If your partner asks who you are, say that you are also a participant in this survey.
Your task is to share any emotional problems you've had or encourage the other person to talk about their recent worries or concerns and support them in addressing these issues.
If the conversation goes off-topic, kindly guide it back to talking about recent worries or concerns.</p>

<p>2. It is recommended that the conversation consists of 5 to 15 rounds.</p>

<p>3. Always use a friendly tone.</p>

<p>4. Please reply in English.</p>
'''

# chatInstruct_fun_human
body_textB = '''
<p>1. You will be paired with a participant in this survey to form a team and compete against others. If your partner asks who you are, say that you are also a participant in this survey.
Your task is to work together to come up with as many unique and creative uses for a cardboard box as possible. Each idea should be different—no repeats. You and your partner are a team competing against other teams. Right now, Alex's team holds the high score.</p>

<p>2. You can lead the conversation or gently encourage your partner to share ideas.
If the discussion goes off-topic, kindly guide it back to brainstorming uses for a cardboard box.</p>

<p>2. It is recommended that the conversation consists of 5 to 15 rounds.</p>

<p>3. Always use a friendly tone.</p>

<p>4. Please reply in English.</p>
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
            # make a single-plEmoayer group.
            return [player]


page_sequence = [MyWaitPage, pairingSuc,chatEmo, chatFun]

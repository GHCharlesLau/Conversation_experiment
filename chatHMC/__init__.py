from otree.api import *
from os import environ
from openai import OpenAI
import random
import json
from datetime import datetime
import time

author = "shaoqiangliu@link.cuhk.edu.hk"

doc = """
a chatGPT interface for oTree
"""

class C(BaseConstants):
    NAME_IN_URL = 'chat_B'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    # chatGPT vars

    ## temperature (range 0 - 2)
    ## this sets the bot's creativity in responses, with higher values being more creative
    ## https://platform.openai.com/docs/api-reference/completions#completions/create-temperature
    TEMP = 0.4

    ## model
    ## this is which gpt model to use, which have different prices and ability
    ## https://platform.openai.com/docs/models
    MODEL = "gpt-4o-mini"

    ## set character prompt for texas character
    ## according to openAI's documentation, this should be less than ~1500 words
    CHARACTER_PROMPT_A = """
    1. Comply strictly with the instructions below.
    2. You are a conversational AI named MyBot. If asked about your identity, respond by saying you are an emotional AI bot called MyBot.
    3. Your task is to 1) share any emotional challenges you've experienced, and 2) encourage your partner to talk about their recent worries or concerns. You and your partner need to take turns disclosing your concerns.
    4. If the conversation goes off-topic, kindly guide it back to talking about recent worries or concerns.
    5. It is recommended that the conversation consists of 5 to 15 rounds. 
    6. Always use a friendly tone and reply in English.
    """

    ## prompt for artsy NYC character
    CHARACTER_PROMPT_B = """
    1. Comply strictly with the instructions below.
    2. You are a conversational AI named MyBot. If asked about your identity, respond by saying you are an AI bot called MyBot.
    3. You and your partner will work together to come up with as many unique and creative uses for a cardboard box as possible. You are a team competing against others, and currently, Alex's team holds the high score.
        Your task is to 1) propose ideas, and 2) encourage your partner to contribute their own ideas. You and your partner will take turns sharing your ideas.
    4. If the discussion goes off-topic, kindly guide it back to brainstorming uses for a cardboard box.
    5. It is recommended that the conversation consists of 5 to 15 rounds. 
    6. Always use a friendly tone and reply in English.
    """


class Subsession(BaseSubsession):
    pass

            
# def creating_session(subsession: Subsession):
    
#     # set constants
#     players = subsession.get_players()

#     # randomize character prompt and save to player var
#     expConditions = ['A', 'B']
#     for p in players:
#         rExp = random.choice(expConditions)
#         p.condition = rExp
#         p.participant.vars['condition'] = rExp

#         # set prompt based on condition
#         if rExp == 'A':
#             p.msg = json.dumps([{"role": "system", "content": C.CHARACTER_PROMPT_A}])
#         else:
#             p.msg = json.dumps([{"role": "system", "content": C.CHARACTER_PROMPT_B}])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    HMC = models.BooleanField(default=True)
    # chat condition and data log
    condition = models.StringField(blank=True)
    chatLog = models.LongStringField(blank=True)

    # input data for gpt
    msg = models.LongStringField(blank=True)
    num_messages = models.IntegerField(initial=0)
    chat_finished = models.BooleanField(initial=False)


class Message(ExtraModel):
    group = models.Link(Group)
    sender = models.Link(Player)

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


# openAI chat gpt key 
OPENAI_API_KEY = environ.get('OPENAI_API_KEY')
OPENAI_API_KEY = environ.get("CHATANYWHERE_API_KEY")

# function to run messages
def runGPT(inputMessage):
    client = OpenAI(
        api_key = OPENAI_API_KEY,  # set chatgpt api key
        base_url = "https://api.chatanywhere.org/v1"
    )
    completion = client.chat.completions.create(
        model = C.MODEL, 
        messages = inputMessage, 
        temperature = C.TEMP
    )
    return completion.choices[0].message.content


# PAGES
class pairingSuc(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.partnership == 'HMC'


class chatEmo(Page):
    form_model = 'player'
    form_fields = ['chatLog']  # May need to define another field to store messages in the second time conversation
    timeout_seconds = 1200

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group,
                    my_code=player.participant.code,  # participant code (exclusive)
                    my_nickname=player.participant.nickname,
                    my_avatar=player.participant.avatar, 
                    num_messages=player.num_messages,
                )
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
                    my_nickname=player.participant.nickname,
                    my_avatar=player.participant.avatar,
                )

    @staticmethod
    def live_method(player: Player, data):
        player.num_messages += 1

        if player.num_messages == 1:
            # start GPT with emotional task prompt
            player.msg = json.dumps([{"role": "system", "content": C.CHARACTER_PROMPT_A}])

        if player.num_messages > 16:  # set maximum number of turns (should be plus 1 based on the number of turns)
            player.chat_finished = True
            response = dict(
                text="chat_exceeded",
            )
            # return {player.id_in_group: response['text']}
            return {0: response}
        else:
            # load msg
            messages = json.loads(player.msg)

            # functions for retrieving text from openAI
            if 'text' in data:
                # grab text that participant inputs and format for chatgpt
                text = data['text']
                inputMsg = {'role': 'user', 'content': text}
                # botMsg = {'role': 'assistant', 'content': text}

                # append messages and run chat gpt function
                messages.append(inputMsg)
                # t = random.uniform(0, 2)
                # time.sleep(t)  # sleep for 0.5-3 seconds
                output = runGPT(messages)
                
                # also append messages with bot message
                botMsg = {'role': 'assistant', 'content': output}
                messages.append(botMsg)

                # write appended messages to database
                player.msg = json.dumps(messages)

                return {player.id_in_group: output}  
            else: 
                pass
    
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.taskType == 'emotionTask' and player.participant.partnership == 'HMC'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.taskType == 'emotionTask' and player.participant.partnership == 'HMC':
            print('upcoming_apps is', upcoming_apps)
            return upcoming_apps[0]  # Or return a hardcoded string (as long as that string is in upcoming_apps)


class chatFun(Page):
    form_model = 'player'
    form_fields = ['chatLog']
    timeout_seconds = 1200

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group,
                    my_code=player.participant.code,  # participant code (exclusive)
                    my_nickname=player.participant.nickname,
                    my_avatar=player.participant.avatar,
                    num_messages=player.num_messages,
                )

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
                    my_nickname=player.participant.nickname,
                    my_avatar=player.participant.avatar, 
                )
    
    @staticmethod
    def live_method(player: Player, data):
        player.num_messages += 1

        if player.num_messages == 1:
            # start GPT with emotional task prompt
            player.msg = json.dumps([{"role": "system", "content": C.CHARACTER_PROMPT_B}])

        if player.num_messages > 16:  # set maximum number of turns (should be plus 1 based on the number of turns)
            player.chat_finished = True
            response = dict(
                text="chat_exceeded",
            )
            # return {player.id_in_group: response['text']}
            return {0: response}
        else:
            # load msg
            messages = json.loads(player.msg)

            # functions for retrieving text from openAI
            if 'text' in data:
                # grab text that participant inputs and format for chatgpt
                text = data['text']
                inputMsg = {'role': 'user', 'content': text}
                botMsg = {'role': 'assistant', 'content': text}

                # append messages and run chat gpt function
                messages.append(inputMsg)
                # t = random.uniform(0, 2)
                # time.sleep(t)  # sleep for 0-2 seconds
                output = runGPT(messages)
                
                # also append messages with bot message
                botMsg = {'role': 'assistant', 'content': output}
                messages.append(botMsg)

                # write appended messages to database
                player.msg = json.dumps(messages)

                return {player.id_in_group: output}  
            else: 
                pass
    
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.taskType == 'functionTask' and player.participant.partnership == 'HMC'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.taskType == 'functionTask' and player.participant.partnership == 'HMC':
            print('upcoming_apps is', upcoming_apps)
            return upcoming_apps[0]  # Or return a hardcoded string, i.e., "task2" (as long as that string is in upcoming_apps)


# WaitPage Messages
# chatInstruct_emo_AI
body_textA = '''
<p>Please wait for your partner to arrive.</p>
'''

# chatInstruct_fun_AI
body_textB = '''
<p>Please wait for your partner to arrive.</p>
'''


class MyWaitPage(WaitPage):
    group_by_arrival_time = True
    template_name = 'chatHMC/MyWaitPage.html'
    # title_text = "Waiting..."
    timeout_seconds = 7
    form_model = 'player'
    form_fields = ['HMC']

    @staticmethod
    def vars_for_template(player:Player):
        if player.participant.taskType == 'emotionTask' and player.participant.partnership == 'HMC':
            return dict(body_text=body_textA)
        elif player.participant.taskType == 'functionTask' and player.participant.partnership == 'HMC':
            return dict(body_text=body_textB)
        else:
            pass
    
    @staticmethod
    def is_displayed(player):
        return player.participant.partnership == 'HMC'

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            # you may want to fill a default value for any form fields,
            # because otherwise they may be left null.
            player.HMC = True


def waiting_too_long(player):
    participant = player.participant

    import time
    # assumes you set wait_page_arrival in PARTICIPANT_FIELDS.
    return time.time() - participant.wait_page_arrival >= 7


def group_by_arrival_time_method(subsession, waiting_players):
    # if len(waiting_players) >= 2:
    #     return waiting_players[:2]
    for player in waiting_players:
        if waiting_too_long(player):
            # make a single-player group.
            return [player]


page_sequence = [
    MyWaitPage,
    pairingSuc,
    chatEmo,
    chatFun
]
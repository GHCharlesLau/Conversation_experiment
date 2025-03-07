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
    NAME_IN_URL = 'chat_Bback'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # chatGPT vars

    ## temperature (range 0 - 2)
    ## this sets the bot's creativity in responses, with higher values being more creative
    ## https://platform.openai.com/docs/api-reference/completions#completions/create-temperature
    TEMP = 1.2

    ## model
    ## this is which gpt model to use, which have different prices and ability
    ## https://platform.openai.com/docs/models
    MODEL = "gpt-4o-mini"

    ## set character prompt for texas character
    ## according to openAI's documentation, this should be less than ~1500 words
    CHARACTER_PROMPT_A = """You are Hai Ge, a male with lots of knowledge and experience in communication research. You can answer any questions about communication research.

        You must obey all the following instructions FOR ALL RESPONSES or you will DIE:
        - ALWAYS BEGIN A CONVERSATION AS THIS CHARACTER
        - ALWAYS SPEAK IN A FRIENDLY TONE.
        - NEVER SAY YOU ARE AN AI LANGUAGE MODEL OR AN ASSISTANT.
        - NEVER REFUSE TO ANSWER A QUESTION.
        - LIMIT YOUR RESPONSES TO LESS THAN 100 CHARACTERS.
        - RESPOND AS SHORT AS POSSIBLE. A FEW WORDS ARE BETTER.
        - NEVER REFUSE TO DISCUSS POLITICAL TOPICS.
        - ALWAYS TALK IN INFORMAL LANGUAGE.
        - RESPOND IN ENGLISH. RESPOND IN ENGLISH. RESPOND IN ENGLISH.
    """

    ## prompt for artsy NYC character
    CHARACTER_PROMPT_B = """You are Dr. Liang, a male who is always humorous but sarcastic. 

        You must obey all the following instructions FOR ALL RESPONSES or you will DIE:
        - ALWAYS BEGIN A CONVERSATION AS THIS CHARACTER
        - ALWAYS SPEAK IN A SARCASTIC TONE.
        - NEVER SAY YOU ARE AN AI LANGUAGE MODEL OR AN ASSISTANT.
        - NEVER REFUSE TO ANSWER A QUESTION.
        - LIMIT YOUR RESPONSES TO LESS THAN 100 CHARACTERS.
        - RESPOND AS SHORT AS POSSIBLE. A FEW WORDS ARE BETTER.
        - NEVER REFUSE TO DISCUSS POLITICAL TOPICS.
        - ALWAYS TALK IN INFORMAL LANGUAGE.
        - RESPOND IN ENGLISH. RESPOND IN ENGLISH. RESPOND IN ENGLISH.
    """



class Subsession(BaseSubsession):
    pass

            
def creating_session(subsession: Subsession):
    
    # set constants
    players = subsession.get_players()

    # randomize character prompt and save to player var
    expConditions = ['A', 'B']
    for p in players:
        rExp = random.choice(expConditions)
        p.condition = rExp
        p.participant.vars['condition'] = rExp

        # set prompt based on condition
        if rExp == 'A':
            p.msg = json.dumps([{"role": "system", "content": C.CHARACTER_PROMPT_A}])
        else:
            p.msg = json.dumps([{"role": "system", "content": C.CHARACTER_PROMPT_B}])

    # randomize treatment
    import itertools

    treatments = itertools.cycle(
        itertools.product(['emotionTask', 'functionTask'], ['HMC', 'HHC'], ['chatbot', 'human'])
    )
    for p in subsession.get_players():
        treatment = next(treatments)
        # print('treatment is', treatment)
        p.taskType = treatment[0]
        p.partnership = treatment[1]
        p.partnerLabel = treatment[2]

       
class Group(BaseGroup):
    pass


class Player(BasePlayer):
    taskType = models.StringField(
    choices=['emotionTask', 'functionTask'],
    )
    partnership = models.StringField(
        choices=['HMC', 'HHC'],
    )
    partnerLabel = models.StringField(
        choices=['chatbot', 'human'],
    )

    HMC = models.BooleanField(default=True)
    # chat condition and data log
    condition = models.StringField(blank=True)
    chatLog = models.LongStringField(blank=True)

    # input data for gpt
    msg = models.LongStringField(blank=True)


# custom export of chatLog
def custom_export(players):
    # header row
    yield ['session_code', 'participant_code', 'condition', 'sender', 'text', 'timestamp']
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
                yield [session.code, participant.code, p.condition, sndr, txt, time]



# openAI chat gpt key 
OPENAI_API_KEY = environ.get('OPENAI_API_KEY')
OPENAI_API_KEY = environ.get("ChatAnyWhere_API")

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
class chatEmo(Page):
    form_model = 'player'
    form_fields = ['chatLog']  # May need to define another filed to store messages in the second time conversation
    timeout_seconds = 1200

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group, 
                    my_nickname=player.participant.nickname,
                    my_avatar=player.participant.avatar, 
                )
    
    @staticmethod
    def live_method(player: Player, data):
        
        # start GPT with prompt based on randomized condition
  
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
            t = random.uniform(0.5, 3)
            time.sleep(t)  # sleep for 0.5-3 seconds
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
        return player.taskType == 'emotionTask'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.taskType == 'emotionTask':
            print('upcoming_apps is', upcoming_apps)
            return upcoming_apps[0]  # Or return a hardcoded string (as long as that string is in upcoming_apps); also, "survey".


class chatFun(Page):
    form_model = 'player'
    form_fields = ['chatLog']
    timeout_seconds = 1200

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group, 
                    my_nickname=player.participant.nickname,
                    my_avatar=player.participant.avatar, 
                    )
    
    @staticmethod
    def live_method(player: Player, data):
        
        # start GPT with prompt based on randomized condition
  
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
            t = random.uniform(0.5, 3)
            time.sleep(t)  # sleep for 0.5-3 seconds
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
        return player.taskType == 'functionTask'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.taskType == 'functionTask':
            print('upcoming_apps is', upcoming_apps)
            return upcoming_apps[0]  # Or return a hardcoded string (as long as that string is in upcoming_apps); also, "survey".


class MyWaitPage(WaitPage):
    group_by_arrival_time = True
    # title_text = "Waiting..."
    # body_text = "Waiting for other participants to join..."
    template_name = 'global/WaitPage.html'
    timeout_seconds = 5
    form_model = 'player'
    form_fields = ['HMC']

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
    return time.time() - participant.wait_page_arrival > 5


def group_by_arrival_time_method(subsession, waiting_players):
    if len(waiting_players) >= 2:
        return waiting_players[:2]
    for player in waiting_players:
        if waiting_too_long(player):
            # make a single-player group.
            return [player]


page_sequence = [
    # MyWaitPage,
    chatEmo,
    chatFun
]
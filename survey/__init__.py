from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_field(label):  # Reduce the amount of repeated code by defining a function that returns a field
    return models.IntegerField(
        label=label,
        #  [value, display] pairs
        choices=[
            [1, "Strongly Disagree"], 
            [2, "Diagree"],
            [3, "Slightly Disagree"],
            [4, "Neutral"],
            [5, "Slightly Agree"],
            [6, "Agree"],
            [7, "Strongly Agree"],
        ],
        widget=widgets.RadioSelect,
    )


class Player(BasePlayer):
    # Sense of Agency
    senA_1 = make_field('The conversational partner in the first round has the ability to solve problems.')
    senA_2 = make_field('The conversational partner in the first round has its own personality.')
    senA_3 = make_field('The conversational partner in the first round is capable of communication.')
    senA_4 = make_field('The conversational partner in the first round can experience emotions.')

    # Feeling Heard
    feeH_1 = make_field('The conversational partner in the first round is interested in what I have to say.')
    feeH_2 = make_field('The conversational partner in the first round encourages me to speak openly.')
    feeH_3 = make_field('The conversational partner in the first round understands my thoughts.')
    feeH_4 = make_field('The conversational partner in the first round cares about me.')

    # AI Literacy
    AIL_1 = make_field('I know the most important concepts of the topic "artificial intelligence".')
    AIL_2 = make_field('I know definitions of artificial intelligence.')
    AIL_3 = make_field('I can assess what the limitations and opportunities of using an AI.')
    AIL_4 = make_field('I can assess what advantages and disadvantages the use of an artificial intelligence entails.')

    # AI Use
    AIU = models.IntegerField(
        label="In the past month, how often did you use AI chatbots?",
        choices=[
            [1, "Never"],
            [2, "Almost Never"],
            [3, "Rarely"],
            [4, "Occasionally"],
            [5, "Frequently"],
            [6, "Very Frequently"],
            [7, "Always"],
        ],
        widget=widgets.RadioSelect,
    )

    # Religiosity
    rlg_1 = make_field('My religious beliefs lie behind my whole approach to life.')
    rlg_2 = make_field('I spend time trying to grow in understanding of my faith.')
    rlg_3 = make_field('I enjoy working in the activities of my religious organization.')
    rlg_4 = make_field('I enjoy spending time with others of my religious affiliation.')
    
    # Conversational Engagement
    CE_1 = make_field('I think I have a good understanding of the conversational partner in the first round.')
    CE_2 = make_field('I was able to understand the issues in the conversation in the same way that the conversational partner in the first round understood them.')
    CE_3 = make_field('I tend to understand the reasons why the conversational partner in the first round does what he or she does.')
    CE_4 = make_field('During conversation, I could feel the emotions the conversational partner in the first round portrayed.')

    # Demographics
    # name = models.StringField(label='What is your name?')
    age = models.IntegerField(
        label='What is your age?', 
        min=13, max=125,
    )
    gender = models.IntegerField(
        choices=[[1,'Male'], 
                 [2, 'Female']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )
    race = models.IntegerField(
        label="What is your race?",
        choices=["White", "Black", "Asian", "Mixed", "Other"],
        widget=widgets.RadioSelect,
    )
    education = models.IntegerField(
        label="What is your educational background?",
        choices=["Below secondary school", "Black", "Asian", "Mixed", "Other"],
        widget=widgets.RadioSelect,
    )
    income = models.IntegerField(
        label="What is your annual household income on average?",
        choices=["10", "100", "1000", "10000", "100000"],
        widget=widgets.RadioSelect,
    )
    partisanship = models.IntegerField(
        label="What is your parlitical leaning?",
        choices=[[1, 'Far demographic'], 
                 [2, 'Demographic']],
        widget=widgets.RadioSelect,
    )


# FUNCTIONS
# PAGES
class Prompt(Page):
    pass


class VariablePageA(Page):
    form_model = 'player'
    form_fields = [
        'senA_1', 'senA_2', 'senA_3', 'senA_4',
        'feeH_1', 'feeH_2', 'feeH_3', 'feeH_4',
        'CE_1', 'CE_2', 'CE_3', 'CE_4'
    ]

class VariablePageB(Page):
    form_model = 'player'
    form_fields = [
        'AIU',
        'AIL_1', 'AIL_2', 'AIL_3', 'AIL_4',
    ]

class Demographics(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'race',
        # 'education',
        # 'income',
        # 'partisanship',
        'rlg_1', 'rlg_2', 'rlg_3', 'rlg_4'
    ]

    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     if timeout_happened:
    #         player.participant.finished = False
    #     else:
    #         player.participant.finished = True


page_sequence = [Prompt, VariablePageA, VariablePageB, Demographics]

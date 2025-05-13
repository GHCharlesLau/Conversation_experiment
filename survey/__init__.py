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
    AIL_2 = make_field('I can assess what the limitations and opportunities of using an AI are.')
    AIL_3 = make_field('I can use AI applications to make my everyday life easier.')
    AIL_4 = make_field('I can use artificial intelligence meaningfully to achieve my everyday goals.')

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
        widget=widgets.RadioSelectHorizontal,
    )

    # Religiosity
    rlg_1 = make_field('My religious beliefs lie behind my whole approach to life.')
    rlg_2 = make_field('I spend time trying to grow in understanding of my faith.')
    rlg_3 = make_field('I enjoy working in the activities of my religious organization.')
    rlg_4 = make_field('I enjoy spending time with others of my religious affiliation.')
    
    # Conversational Engagement
    CE_1 = make_field('During conversation, I could feel the emotions the conversational partner in the first round portrayed.')
    CE_2 = make_field('The conversation with the partner in the first round was enjoyable.')
    CE_3 = make_field('I was mentally involved in the conversation with the partner in the first round.')
    CE_4 = make_field('While engaged in the converation, I had a vivid image of the partner in the first round.')

    # Demographics
    # name = models.StringField(label='What is your name?')
    age = models.IntegerField(
        label='<b>What is your age?</b>', 
        min=13, max=125,
    )
    gender = models.StringField(
        label='<b>What is your gender?</b>',
        choices=['Man', 
                 'Woman',
                 'Nonbinary',
                 'Something else'
                 ],
        widget=widgets.RadioSelect,
    )
    race = models.StringField(
        label="<b>Which race do you belong to?</b>",
        choices=["White", "Black or African American", "American Indian or Alaska Native", "Asian", "Native Hawaiian or other Pacific Islander", "Other"],
        widget=widgets.RadioSelect,
    )
    education = models.StringField(
        label="<b>What is the highest level of school you have completed or the highest degree you have received?</b>",
        choices=["Less than high school credential", 
                 "High school graduate - High school diploma or equivalent (e.g., GED)", 
                 "Some college but no degree",
                 "Associate degree in college - Occupational/vocational program",
                 "Associate degree in college - Academic program",
                 "Bachelor's degree (e.g., BA, AB, BS)",
                 "Master's degree (e.g., MA, MS, MEng, MEd, MSW, MBA)",
                 "Professional school degree (e.g., MD, DDS, DVM, LLB, JD)",
                 "Doctorate degree (e.g., PhD, EdD)",
                 "Other"],
        widget=widgets.RadioSelect,
    )
    income = models.StringField(
        label="<b>What was the total income of your family during the past 12 months before taxes?</b>",
        choices=["Less than $5,000",
                 "$5,000 to $7,499",
                 "$7,500 to $9,999",
                 "$10,000 to $12,499",
                 "$12,500 to $14,999",
                 "$15,000 to $19,999",
                 "$20,000 to $24,999",
                 "$25,000 to $29,999",
                 "$30,000 to $34,999",
                 "$35,000 to $39,999",
                 "$40,000 to $49,999",
                 "$50,000 to $59,999",
                 "$60,000 to $74,999",
                 "$75,000 to $99,999",
                 "$100,000 to $149,999",
                 "$150,000 or more"
                 ],
        widget=widgets.RadioSelect,
    )
    partisanship = models.StringField(
        label="<b>Do you usually think of yourself as a Democrat, a Republican, an independent, or what?</b>",
        choices=["Democrat",
                 "Republican",
                 "Independent",
                 "Other"
                 ],
        widget=widgets.RadioSelect,
    )

    # Manipulation check
    partner_label = models.StringField(
        label="",
        choices=["Another participant in this survey", "An AI partner named MyBot", "I don't know"],
        widget=widgets.RadioSelect,
    )

    # Open-ended question (for the pilot study)
    open_ended = models.LongStringField(
        label="<b>Could you leave any additional comments or suggestions for this study? Your suggestions are important to us!</b><hr>",
        blank=True
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
        'CE_1', 'CE_2', 'CE_3', 'CE_4',
    ]

class VariablePageB(Page):
    form_model = 'player'
    form_fields = [
        'partner_label',
        'AIU',
        'AIL_1', 'AIL_2', 'AIL_3', 'AIL_4',
        'open_ended'
    ]

class Demographics(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'race',
        'education',
        'income',
        'partisanship',
        'rlg_1', 'rlg_2', 'rlg_3', 'rlg_4'
    ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant.finished = False
        else:
            player.participant.finished = True


page_sequence = [Prompt, VariablePageA, VariablePageB, Demographics]

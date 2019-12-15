#!/usr/bin/env python3

import chatterbot
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import filters
from chatterbot import comparisons
from chatterbot import response_selection
import anki_vector
from anki_vector.util import degrees
import cozmo
import time
import nltk
import ssl

# work around some NLTK download weirdness
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

chatbot1 = ChatBot(
    'Inky',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///chatbotinkydb.sqlite3',
    filters=[filters.get_recent_repeated_responses],
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": comparisons.levenshtein_distance,
            "response_selection_method": response_selection.get_random_response
        }
    ],
    tie_breaking_method="random_response"
)

chatbot2 = ChatBot(
    'Blinky',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///chatbotblinkydb.sqlite3',
    filters=[filters.get_recent_repeated_responses],
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": comparisons.sentiment_comparison,
            "response_selection_method": response_selection.get_random_response
        }
    ],
    tie_breaking_method="random_response"
)

# create trainers and train the bots (only needs to be done once)
# trainer1 = ChatterBotCorpusTrainer(chatbot1)
# trainer2 = ChatterBotCorpusTrainer(chatbot2)
# trainer1.train("chatterbot.corpus.english")
# trainer2.train("chatterbot.corpus.english")

def main(robot: cozmo.robot.Robot):
    robot1 = anki_vector.Robot()
    robot1.connect()
    seed="Hi, how is it going?"
    print(seed)
    response1 = seed
    robot1.behavior.say_text(str(response1),use_vector_voice=True,duration_scalar=1.0)

    while True:
        response2 = chatbot2.get_response(response1)
        print(response2)
        robot.say_text(str(response2)).wait_for_completed()
        response1 = chatbot1.get_response(response2)
        print(response1)
        robot1.behavior.say_text(str(response1), use_vector_voice=True,duration_scalar=1.0)

cozmo.run_program(main)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings

from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.events import SlotSet
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.keras_policy import KerasPolicy

logger = logging.getLogger(__name__)

agentModelPath='models/dialogue'

def trainDialogue(domainFile='domain/domain.yml',
                  modelPath=agentModelPath,
                  trainingDataFile='data/stories.md'):
    agent = Agent(DomainFile,
                  policies=[MemoizationPolicy(), KerasPolicy()])
    
    agent.train(TrainingDataFile,
                max_history=3,
                epochs=400,
                batch_size=100,
                validation_split=0.2)

    agent.persist(ModelPath)
    return agent

def run(serve_forever=True,
        nluModelDirectory):
    interpreter = RasaNLUInterpreter(nluModelDirectory)
    agent = Agent.load(agentModelPath, interpreter=interpreter)

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
    return agent

if __name__ == '__main__':
    utils.configure_colored_logging(loglevel='INFO')

    parser = argparse.ArgumentParser(
        description='Starts the bot.'
    )

    parser.add_argument(
        'task',
        choices=['train', 'run'],
        help='What the bot should do =- e.g. train or run?'
    )

    task = parser.parse_args().task

    if task == 'train':
        trainDialogue()
    elif task == 'run':
        run()
    else:
        warnings.warn('Need to either pass "train" or "run" to use this script')

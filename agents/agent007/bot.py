from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings
import domain.buildDomain

from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.channels.console import ConsoleOutputChannel
from rasa_core.events import SlotSet
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.keras_policy import KerasPolicy

logger = logging.getLogger(__name__)

agentModelPath='models/dialogue'

def trainDialogue(domainFile='domain/domain.yml',
                  modelPath=agentModelPath,
                  trainingDataFile='data/stories.md'):
    agent = Agent(domainFile,
                  policies=[MemoizationPolicy(), KerasPolicy()])
    
    agent.train(trainingDataFile,
                max_history=3,
                epochs=400,
                batch_size=100,
                validation_split=0.2)

    agent.persist(modelPath)
    return agent

def run(nluModelDirectory,
        serve_forever=True):
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
        '-t',
        required=True,
        choices=['train', 'run', 'build_train'],
        help='What the bot should do =- e.g. train, run, or build domain and train ("build_train")?'
    )

    parser.add_argument(
        '-n',
        help='The location of the nlu model directory'
    )

    task = parser.parse_args().t
    
    if task == 'train':
        trainDialogue()
    elif task == 'run':
        nlu_model_dir = parser.parse_args().n
        if nlu_model_dir == None:
            warnings.warn('When passing "-t run," you must also pass the -n parameter for the location of the nlu model directory.')
        else:
            run(nlu_model_dir)
    elif task == 'build_train':
        domain.buildDomain.build_domain()
        trainDialogue()
    else:
        warnings.warn('Invalid -t argument.  You must use either train, run, or build_train.')

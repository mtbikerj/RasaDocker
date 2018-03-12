from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.agent import Agent

import argparse
import os

domainFile = "domain/domain.yml"
trainingStories = "stories.md"
modelPath = "models/dialog"
nluModelDir = "../../nlu/models/default/default"

def train():
    agent = Agent(domainFile, policies=[MemoizationPolicy(), KerasPolicy()])
    agent.train(
        trainingStories,
        max_history = 3,
        epochs = 100,
        batch_size = 10,
        augmentation_factor = 20,
        validation_split = 0.2,
        remove_duplicates = True
    )
    agent.persist(modelPath)

def run():
    interpreter = RasaNLUInterpreter(model_directory = nluModelDir)
    agent = Agent.load(modelPath, interpreter = interpreter)
    agent.handle_channel(ConsoleInputChannel())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="starts the bot")
    parser.add_argument("-t",
                        choices=["train", "run_console"],
                        help="what the bot should do")

    task = parser.parse_args().t

    if task == "train":
        train()
    elif task == "run_console":
        print(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
        run()
    else:
        warnings.warn("Need to pass 'train' as argument")
        exit(1)
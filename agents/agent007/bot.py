from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.agent import Agent
from rasa_core.channels.rest import HttpInputChannel
from CustomWebChannel import CustomWebChannel

import argparse

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

def run(channel = 'console'):
    interpreter = RasaNLUInterpreter(model_directory = nluModelDir)
    agent = Agent.load(modelPath, interpreter = interpreter)
    if (channel == 'console'):
        agent.handle_channel(ConsoleInputChannel())
    else:
        input_channel = CustomWebChannel()
        http_channel = HttpInputChannel(4000, '/', input_channel)
        agent.handle_channel(http_channel)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="starts the bot")
    parser.add_argument("-t",
                        choices=["train", "run_console", "run_http"],
                        help="what the bot should do")

    task = parser.parse_args().t

    if task == "train":
        train()
    elif task == "run_console":
        run()
    elif task == "run_http":
        run('http')
    else:
        warnings.warn("Need to pass 'train' or 'run_console' as argument")
        exit(1)
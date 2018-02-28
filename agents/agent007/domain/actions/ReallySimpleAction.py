from rasa_core.actions.action import Action

import requests

class ReallySimpleAction(Action):
    
    def name(self):
        return 'ActionReallySimpleAction'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("The Really Simple Action was just called")
        return []


                            
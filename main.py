import random
import numpy as np
import pickle
from response import Response
import pyttsx3 as ts
from survey import survey
from survey import show_loading
class Bot:
    def __init__(self):
        with open('model_pickel', 'rb') as f:
            self.model = pickle.load(f)

    def bot_initialize(self):
        voices = ts.init().getProperty('voices')
        print("Initializing the engine...")
        Response.speak("Initializing the engine...")

        name = input('Enter your name: ')

        greetings = [f"Hi {name}! I'm Gradify. Your academic performance assistant.",
            f"Hello {name}! I'm Gradify. I'll be helping you understand your study habits today.",
        f"Hey {name}! I'm Gradify, your personal academic companion."]
        intro = [random.choice(greetings),"I'll ask you a few quick questions about your daily routine to estimate your academic performance...",
        "This short survey will help us predict your expected GPA and stress level...",
        "Answer honestly and I'll try to give you helpful suggestions at the end."]
        for item in intro:
            print(item.capitalize())
        Response.speak(intro)

    def main(self):
        self.bot_initialize()
        while True:
            user_data = survey()
            if user_data['user_data'].sum() > 24:
                print("You can not add more than 24 hours in all categories because it is impossible for a day.\n You have to give the survey again or you can enter 'exit' to get off.")
                user_response = input("Do you want to give the survey one more time or not. (Enter Yes or No)").lower()
                if user_response == 'no':
                    user_data['user_data'] = np.array([])
                    user_data['user_text'] = 'Nothing here'
                else:
                    continue
            break

        if user_data['user_data'].size != 0:
            show_loading("Prepairing your Data.... Making predictions..." )
            predicted_gpa = self.model.predict(user_data['user_data'])
            response = Response(user_data)
            adjusted_gpa = response.adjust_gpa(user_data['user_text'],predicted_gpa)
            show_loading("Generating Response.....This may take a while..." )
            sentences = response.generate_response(adjusted_gpa)
            for sentence in sentences:
                print(sentence)
                response.speak(sentence)
            response.get_and_respond("If you have any other queries about your studies or time management feel free to ask.")

Gradify = Bot()
Gradify.main()
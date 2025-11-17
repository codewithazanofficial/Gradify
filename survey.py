import numpy as np
def survey():
    print(
        "========== Survey =========\n'The Survey is now going to proceed if you want to exit anytime you can type 'exit' while giving answers.'")
    while True:
        try:
            q = 1
            question = input(f"Q#{q}:\nRoughly how many hours do you study on a normal day?: ")
            study_hours = float(question)
            q += 1
            question = input(
                f"Q#{q}:\nHow many hours do you spend daily on extracurricular activities like clubs, competitions, or creative hobbies?: ")
            eca_hours = float(question)
            q += 1
            print("Alright, next question's about your sleep — everyone's favorite topic.")
            question = input(f"Q#{q}:\nHow many hours of sleep do you usually get at night?: ")
            sleep_hours = float(question)
            q += 1
            print("Cool! Now let's talk about your social side for a minute.")
            question = input(
                f"Q#{q}:\nOn an average, how many hours go into talking with friends or being online socially— in hours?: ")
            social_hours = float(question)
            q += 1
            print("Great! only a couple of questions left...")
            question = input(f"Q#{q}:\nDo you work out or play any sports? About how many hours daily?: ")
            physical_hours = float(question)
            user_text = input(
                "Please describe in a few sentences how you feel about studying this subject. Be honest — you can write 2–5 lines.")
            break
        except ValueError:
            if question.lower() == "exit":
                print("Thank you for joining.")
                break
            else:
                print("Oops a number was expected.")
    user_data = {
        'user_data': np.array([study_hours, eca_hours, sleep_hours, social_hours, physical_hours]).reshape(1, -1),
        'user_text': user_text
        }
    return user_data
import time
import sys

def show_loading(message, duration=3):
    print(message, end="")
    for _ in range(duration):
        for dot in "...":
            sys.stdout.write(dot)
            sys.stdout.flush()
            time.sleep(0.4)
        sys.stdout.write("\b\b\b   \b\b\b")  # Erase dots

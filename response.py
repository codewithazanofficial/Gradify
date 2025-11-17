
import google.generativeai as genai
import pyttsx3 as ts
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# Configure API key
genai.configure(api_key="your_api_key")

# Create the model
model = genai.GenerativeModel("gemini-2.5-flash")

# Example data (you’ll pass real data from your model)
class Response:
    def __init__(self,user_data):
        self.user_data = user_data['user_data'].ravel()
        self.study_hours = self.user_data[0]
        self.extracurricular_hours = self.user_data[1]
        self.sleep_hours = self.user_data[2]
        self.social_hours = self.user_data[3]
        self.physical_hours = self.user_data[4]
        self.user_text = user_data['user_text']
    def generate_response(self,gpa):
        self.gpa = gpa
        prompt = f"""
        You are Gradify, an analytical academic performance evaluator.
        
        A student has submitted the following daily lifestyle data:
        
        - Study Hours: {self.study_hours}
        - Extracurricular Hours: {self.extracurricular_hours}
        - Sleep Hours: {self.sleep_hours}
        - Social Hours: {self.social_hours}
        - Physical Activity Hours: {self.physical_hours}
        - Predicted GPA: {self.gpa}
        - User Interest: {self.user_text}
        Your task:
        1. Analyze the numbers logically and directly — no unnecessary praise or emotion, honestly first state the gpa and a short comment about it.
        2. Comment straight forward and honestly on gpa.
        3. Identify any weak areas (e.g., too little sleep, excessive social time, low study hours).
        4. For each weak habit, give a clear numeric suggestion for improvement (e.g., “Increase study time to 7–8 hours” or “Reduce social hours to below 2 per day”).
        5. Provide reasoning for each suggestion briefly and factually.
        6. Conclude with an estimated improvement in GPA if the recommendations are followed.
        7. Keep the total response under 8 sentences, concise and professional.
        8. Also keep that the the study hours have a correlation 0.73 and physical hours have a correlation of 0.34 while the other factors have a negligible effect according to the data i have and i want you to focus more on these two entities but don't mention technical aspects like correlation in the response.
        Instructions:
        1. Be honest, criticise where it is needed.
        2. Consider that for study hours the best range is 9 to 11 hours per day so don't criticise if they are in this range but appriciate. If not in this range then criticise.
        3. Consider that for extracurricular hours the best range is 1 to 2.5 hours per day so don't criticise if they are in this range but appriciate. If not in this range then criticise.
        4. Consider that for sleep hours the best range is 7 to 8 hours per day so don't criticise if they are in this range but appriciate. If not in this range then criticise.
        5. Consider that for social hours the best range is 1 to 2.5 hours per day so don't criticise if they are in this range but appriciate. If not in this range then criticise.
        6. 2. Consider that for physical hours the best range is 1 to 3 hours per day so don't criticise if they are in this range but appriciate. If not in this range then criticise.
        """
        response = model.generate_content(prompt)
        sentences = sent_tokenize(response.text)
        return sentences
    @staticmethod
    def speak(response, voice = None, rate = 180, volume = 1.0):
        engine = ts.init()
        if voice:
            voices = engine.getProperty('voices')
            for i in voices:
                if voice in i.id:
                    engine.setProperty('voice',voice)
        engine.setProperty('rate',rate)
        engine.setProperty('volume',volume)
        engine.say(response)
        engine.runAndWait()

    def adjust_gpa(self,user_text, predicted_gpa):
        analyzer = SentimentIntensityAnalyzer()
        ps = analyzer.polarity_scores(user_text)
        return ps['compound'] * 0.4 + predicted_gpa

    def get_and_respond(self, text = ""):
        if text == "":
            print("Do you have any more questions (enter exit to end the conversation.)", end=':')
        else:
            print(text,"(enter exit to end the conversation.)" ,end=':')
            self.speak(text)
        user_question = input("")
        if user_question.lower() == 'exit':
            print("Thanks for your time, and remember — small, but consistent efforts matter most\nSee you next time, till then stay focused!")
            self.speak("Thanks for your time, and remember small, but consistent efforts matter most. See you next time, till then, stay focused!")
            return None
        prompt = f"""You are Gradify, an intelligent academic assistant. 
        Answer the user’s question clearly, briefly, and accurately. 
        Focus on helpful academic or personal productivity advice. 
        Keep your tone friendly but concise — around 2 to 3 sentences maximum. 
        If the question is unclear or unrelated to academics or learning, politely guide the user back to relevant topics.
        User’s question: {user_question}
        Extras:
        While giving response you can use the data given below if needed as context:
        The user's Predicted GPA is {self.gpa}. 
        Here is their activity data: {self.user_data}. 
        Note:
        Only use the references of the above data in the response if user asks for or if needed. 
        """
        passage = model.generate_content(prompt)
        sentences = sent_tokenize(passage.text)
        for sentence in sentences:
            print(sentence)
            self.speak(sentence)
        self.get_and_respond()

# a = Response(user_data,gpa=3.1)
if __name__ == '__main__':
    voices = ts.init().getProperty('voices')
    print("Initializing the engine.")
    import numpy as np
    user_data = {
        'user_data': np.array([[5.2, 6.5, 3.2, 3.6, 1.2]]),
        'user_text': "I love my subject and i am very passionate."
    }
    Response.speak("Initializing the engine...",voices[1].id,170)
    # # Print the generated text
    # print("\nGenerated Advice:\n")
    a = Response(user_data)
    a.get_and_respond("If you have any queries related to your studies you can ask freely.")


